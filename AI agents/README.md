# AI Agent with Gemini Pro

This project implements an intelligent AI agent using Google's Gemini Pro API. The agent can analyze tasks, create execution plans, and learn from interactions. It includes both JavaScript and Python implementations with a Streamlit web interface.

## Features

- 🤖 Task Analysis & Planning
- 🧠 Memory & Learning Capabilities
- 💬 Streaming Content Generation
- 📊 Interactive Web Interface
- 📝 Conversation History
- 📈 Performance Insights

## Prerequisites

- Node.js (for JavaScript version)
- Python 3.8+ (for Python/Streamlit version)
- Google Gemini Pro API key

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Install Dependencies**

   For Python/Streamlit version:
   ```bash
   pip install -r requirements.txt
   ```

   For JavaScript version:
   ```bash
   npm install
   ```

3. **Configure API Key**

   Create a `.env` file in the root directory and add your Gemini Pro API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Python/Streamlit Version

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Enter your task in the text area and click Submit

### JavaScript Version

1. Run the example script:
   ```bash
   node example.js
   ```

## Project Structure

```
├── src/
│   ├── components/
│   │   └── AIAgent.js         # Main agent implementation (JS)
│   ├── utils/
│   │   └── geminiService.js   # Gemini API service (JS)
│   └── tests/
│       └── aiAgent.test.js    # Test suite
├── ai_agent.py                # Python implementation
├── app.py                     # Streamlit web interface
├── example.js                 # JS usage example
├── requirements.txt           # Python dependencies
└── .env                      # Environment variables
```

## Features Explained

### Task Analysis
The agent breaks down complex tasks into manageable components and creates a structured plan for execution.

### Memory System
- Conversation History: Tracks all interactions
- Task History: Records completed tasks and their analyses
- Learning System: Stores successful patterns and error cases

### Content Generation
- Regular content generation
- Streaming capabilities for real-time responses
- Chat conversation support

## API Reference

### JavaScript Version

```javascript
const agent = new AIAgent();

// Execute a task
const response = await agent.executeTask('Your task here');

// Get streaming content
const streamResponse = await agent.streamTask('Your task here');

// Get agent insights
const insights = await agent.getInsights();
```

### Python Version

```python
agent = AIAgent()

# Execute a task
response = await agent.execute_task("Your task here")

# Access memory and insights
insights = agent.memory
```

## Error Handling

The system includes comprehensive error handling:
- API key validation
- Task execution monitoring
- Error logging and learning
- Graceful failure recovery

## Best Practices

1. **API Key Security**
   - Never commit your API key
   - Use environment variables
   - Keep your `.env` file private

2. **Memory Management**
   - Monitor memory usage for long-running sessions
   - Clear conversation history if needed

3. **Task Complexity**
   - Break down complex tasks
   - Use specific, clear instructions
   - Check agent insights for performance

## Troubleshooting

Common issues and solutions:

1. **API Key Error**
   - Ensure `.env` file exists
   - Verify API key is correct
   - Check environment variable loading

2. **Memory Issues**
   - Restart the agent for a fresh state
   - Monitor memory usage
   - Clear conversation history if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini Pro API
- Streamlit Framework
- Node.js Community

## Support

For support, please open an issue in the repository or contact the maintainers.