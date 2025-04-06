import streamlit as st
import requests

# Remove the PyDictionary import and use only the Dictionary API
def get_word_details(word):
    """
    Get word details from Dictionary API
    """
    try:
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(api_url)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def format_definitions(data):
    """
    Format the definitions from API response
    """
    meanings = {}
    if data:
        for meaning in data[0]['meanings']:
            pos = meaning['partOfSpeech']
            definitions = [d['definition'] for d in meaning['definitions']]
            meanings[pos] = definitions
    return meanings

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Dictionary App",
        page_icon="📚",
        layout="wide"
    )

    # Main title
    st.title("📚 Dictionary App")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info(
        "This is a dictionary app that helps you find meanings, "
        "pronunciations, and examples of words. It uses the Free Dictionary API."
    )

    # Search box
    word = st.text_input("Enter a word:", "")

    if word:
        with st.spinner(f'Searching for "{word}"...'):
            data = get_word_details(word)

        if data:
            # Create two columns
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📖 Meanings and Definitions")
                meanings = format_definitions(data)
                
                for pos, definitions in meanings.items():
                    st.markdown(f"**{pos.title()}**")
                    for definition in definitions:
                        st.markdown(f"• {definition}")
                    st.markdown("---")

            with col2:
                st.subheader("🔤 Word Details")
                
                # Display phonetics
                if 'phonetic' in data[0]:
                    st.markdown(f"**Pronunciation:** {data[0]['phonetic']}")

                # Display audio if available
                for phonetic in data[0].get('phonetics', []):
                    if 'audio' in phonetic and phonetic['audio']:
                        st.audio(phonetic['audio'])
                        break

            # Examples and Synonyms
            st.subheader("📝 Examples and Synonyms")
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("**Examples:**")
                examples_found = False
                for meaning in data[0].get('meanings', []):
                    for definition in meaning.get('definitions', []):
                        if 'example' in definition:
                            st.markdown(f"• {definition['example']}")
                            examples_found = True
                if not examples_found:
                    st.info("No examples available.")

            with col4:
                st.markdown("**Synonyms:**")
                synonyms = set()
                for meaning in data[0].get('meanings', []):
                    synonyms.update(meaning.get('synonyms', []))
                if synonyms:
                    for synonym in list(synonyms)[:5]:
                        st.markdown(f"• {synonym}")
                else:
                    st.info("No synonyms available.")

            # Save word feature
            if st.button("Save Word"):
                saved_words = st.session_state.get('saved_words', [])
                if word not in saved_words:
                    saved_words.append(word)
                    st.session_state['saved_words'] = saved_words
                    st.success(f"'{word}' has been saved!")
                else:
                    st.info(f"'{word}' is already saved!")

        else:
            st.error("Word not found. Please check the spelling.")

    # Display saved words in sidebar
    st.sidebar.header("Saved Words")
    if 'saved_words' in st.session_state and st.session_state['saved_words']:
        for saved_word in st.session_state['saved_words']:
            if st.sidebar.button(saved_word):
                st.text_input("Enter a word:", value=saved_word)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Created with ❤️ using Free Dictionary API</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 