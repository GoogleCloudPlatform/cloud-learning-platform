import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// Mock data for chat history
const chatHistory = [
  { id: 1, message: 'Hello, how can I help you today?' },
  { id: 2, message: 'Can you tell me about the weather?' },
  { id: 3, message: 'Sure, it is currently sunny with a high of 75 degrees.' },
];

// Mock data for models
const chatModels = ['Model 1', 'Model 2', 'Model 3'];

interface ChatResponse {
  content: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'chat-app';
  selectedModel = chatModels[0];
  message = '';
  chats = chatHistory;
	models = chatModels;

  constructor(private http: HttpClient) {}

  sendMessage() {
    this.http.post<ChatResponse>('https://your-chat-service.com/api', {
      llm_type: this.selectedModel,
      prompt: this.message
    }).subscribe(response => {
      this.chats.push({ id: Date.now(), message: response['content'] });
      this.message = '';
    }, error => {
      console.error(error);
    });
  }
}
