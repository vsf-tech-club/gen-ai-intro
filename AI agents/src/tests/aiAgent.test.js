const AIAgent = require('../components/AIAgent');

async function testAIAgent() {
    const agent = new AIAgent();
    
    try {
        // Test regular content generation
        console.log('Testing content generation...');
        const result = await agent.executeTask('What are the benefits of sustainable energy?');
        console.log('Response:', result);

        // Test streaming content
        console.log('\nTesting streaming content...');
        const streamResult = await agent.streamTask('Explain quantum computing in simple terms.');
        console.log('Streaming complete');

    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
testAIAgent();