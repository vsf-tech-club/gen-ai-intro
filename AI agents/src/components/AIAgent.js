const GeminiService = require('../utils/geminiService');

class AIAgent {
    constructor() {
        this.geminiService = new GeminiService();
        this.memory = {
            conversationHistory: [],
            taskHistory: [],
            learnings: new Map()
        };
        this.currentTask = null;
    }

    async executeTask(task) {
        try {
            this.currentTask = task;
            
            const taskAnalysis = await this.analyzeTask(task);
            
            this.memory.taskHistory.push({
                task,
                timestamp: new Date(),
                analysis: taskAnalysis
            });

            const response = await this.generateAndExecutePlan(taskAnalysis);
            
            await this.learnFromExecution(task, response);
            
            return response;
        } catch (error) {
            console.error('Error executing task:', error);
            this.memory.learnings.set(`error_${Date.now()}`, {
                task,
                error: error.message,
                timestamp: new Date()
            });
            throw error;
        }
    }

    async analyzeTask(task) {
        const analysisPrompt = `Analyze this task and break it down into steps:
        Task: ${task}
        Consider:
        1. What are the main components of this task?
        2. What knowledge is required?
        3. What potential challenges might arise?
        Please provide a structured analysis.`;

        return await this.geminiService.generateContent(analysisPrompt);
    }

    async generateAndExecutePlan(analysis) {
        const planPrompt = `Based on this analysis: ${analysis}
        Create a step-by-step plan to accomplish the task.
        Include any necessary validations or error checks.`;

        const plan = await this.geminiService.generateContent(planPrompt);
        
        return await this.geminiService.generateContent(
            `${plan}\n\nNow, execute this plan for: ${this.currentTask}`
        );
    }

    async learnFromExecution(task, result) {
        this.memory.learnings.set(`success_${Date.now()}`, {
            task,
            result,
            timestamp: new Date()
        });

        this.memory.conversationHistory.push({
            role: 'user',
            content: task
        }, {
            role: 'assistant',
            content: result
        });
    }

    async streamTask(task) {
        try {
            const contextualPrompt = `Taking into account previous interactions:
            ${JSON.stringify(this.memory.learnings)}
            
            Current task: ${task}`;
            
            return await this.geminiService.generateStreamingContent(contextualPrompt);
        } catch (error) {
            console.error('Error streaming task:', error);
            throw error;
        }
    }

    async getInsights() {
        return {
            tasksCompleted: this.memory.taskHistory.length,
            learningEntries: this.memory.learnings.size,
            conversationTurns: this.memory.conversationHistory.length
        };
    }
}

module.exports = AIAgent;