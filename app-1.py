import gradio as gr
from groq import Groq  # Assuming you have a Groq Python client library
from textblob import TextBlob

# Replace this with your Groq API key
groq_api_key = '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'

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Function to generate a response from Groq
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Replace with the appropriate Groq model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Access the content attribute of the message object
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

# Provide coping strategies
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")

# Chatbot function
def chatbot(user_message, history):
    # Analyze sentiment of the user's message
    sentiment, polarity = analyze_sentiment(user_message)
    
    # Generate a response from Groq
    bot_response = generate_response(user_message)
    
    # Provide a coping strategy based on sentiment
    coping_strategy = provide_coping_strategy(sentiment)
    
    # Update the chat history (using OpenAI-style 'role' and 'content' format)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": bot_response})
    
    # Prepare the output (chat history + sentiment analysis + coping strategy)
    output = (
        f"Sentiment: {sentiment} (Polarity: {polarity})\n"
        f"Suggested Coping Strategy: {coping_strategy}"
    )
    
    return history, output, ""  # Return an empty string to clear the input box

# Gradio Interface
with gr.Blocks(theme = 'Respair/Shiki@1.2.1') as demo:
    gr.Markdown("# Mental Health Support Chatbot")
    
    # Add a calming song using gr.Audio
    gr.Markdown("## Listen to a Calming Song")
    calming_song = gr.Audio(
        value="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",  # Replace with your own MP3 file URL
        label="Calming Background Music",
        autoplay=False,  # Set to True if you want the song to play automatically
        loop=True  # Loop the song continuously
    )
    
    # Chat history display
    chat_history = gr.State([])  # State to store chat history
    chat_display = gr.Chatbot(label="Chat History", type="messages")  # Use type='messages'
    
    # User input
    user_input = gr.Textbox(label="You:", placeholder="Type your message here...")
    
    # Output area for sentiment and coping strategy
    output_text = gr.Textbox(label="Analysis and Coping Strategy")
    
    # Submit button
    submit_button = gr.Button("Send")
    
    # Disclaimer (using gr.HTML for styled HTML)
    gr.HTML("""
    <h2 style='color: #FF5733;'>Data Privacy Disclaimer</h2>
    <span style='color: #FF5733;'>
    This application stores your session data, including your messages and sentiment analysis results, 
    in temporary storage during your session. This data is not stored permanently and is used solely 
    to improve your interaction with the chatbot. Please avoid sharing personal or sensitive information 
    during your conversation.
    </span>
    """)
    
    # Resources (plain Markdown)
    gr.Markdown("""
    ### Resources
    If you need immediate help, please contact one of the following resources:
    - National Suicide Prevention Lifeline: 1-800-273-8255
    - Crisis Text Line: Text 'HELLO' to 741741
    - [More Resources](https://www.mentalhealth.gov/get-help/immediate-help)
    """)

    # Button action
    submit_button.click(
        chatbot,
        inputs=[user_input, chat_history],
        outputs=[chat_display, output_text, user_input]  # Include user_input to clear it
    )

    # Add support for the "Enter" key
    user_input.submit(
        chatbot,
        inputs=[user_input, chat_history],
        outputs=[chat_display, output_text, user_input]  # Include user_input to clear it
    )

# Launch the Gradio app
demo.launch(share=True)