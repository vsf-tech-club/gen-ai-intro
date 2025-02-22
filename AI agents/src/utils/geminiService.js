const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class GeminiService {
    constructor() {
        if (!process.env.GEMINI_API_KEY) {
            throw new Error('GEMINI_API_KEY environment variable is not set');
        }
        
        this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
        const generationConfig = {
            temperature: 1,
            topP: 0.95,
            topK: 40,
            maxOutputTokens: 8192,
        };
        
        this.model = this.genAI.getGenerativeModel({ 
            model: "gemini-2.0-flash-exp",
            generationConfig,
        });
    }

    async generateContent(prompt) {
        try {
            const result = await this.model.generateContent(prompt);
            const response = await result.response;
            return response.text();
        } catch (error) {
            console.error('Error generating content:', error);
            throw error;
        }
    }

    async generateStreamingContent(prompt) {
        try {
            const result = await this.model.generateContentStream(prompt);
            let fullResponse = '';
            
            for await (const chunk of result.stream) {
                const chunkText = chunk.text();
                fullResponse += chunkText;
                console.log(chunkText);
            }
            
            return fullResponse;
        } catch (error) {
            console.error('Error in streaming content:', error);
            throw error;
        }
    }

    async chatConversation(messages) {
        try {
            const chat = this.model.startChat();
            const result = await chat.sendMessage(messages);
            return result.response.text();
        } catch (error) {
            console.error('Error in chat conversation:', error);
            throw error;
        }
    }
}

module.exports = GeminiService;