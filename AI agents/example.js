const AIAgent = require('./src/components/AIAgent');

async function runExample() {
    const agent = new AIAgent();
    try {
        console.log('=== AI Agent Demo ===\n');
        
        // Complex task that requires analysis and planning
        const task = `Create a comprehensive study plan for someone learning artificial intelligence. 
                     Include key topics, estimated time frames, and recommended resources. 
                     Consider both theoretical knowledge and practical implementation.`;
        
        console.log('Given Task:', task, '\n');
        console.log('Agent is analyzing and creating a plan...\n');
        
        const response = await agent.executeTask(task);
        console.log('Final Response:', response, '\n');

        // Show what the agent has learned
        const insights = await agent.getInsights();
        console.log('Agent Insights:', JSON.stringify(insights, null, 2));

        // Try a related follow-up task to demonstrate memory usage
        console.log('\nTrying a related follow-up task...');
        const followUpTask = 'What programming languages would be most important for the AI curriculum you just created?';
        const followUpResponse = await agent.executeTask(followUpTask);
        console.log('\nFollow-up Response:', followUpResponse);

    } catch (error) {
        console.error('Error:', error.message);
    }
}

runExample();