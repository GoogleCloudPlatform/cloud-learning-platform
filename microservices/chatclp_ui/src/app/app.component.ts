import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// Mock data for chat history
const chatHistory = [
  { id: 1, message: 'Hello, how can I help you today?' },
  { id: 2, message: 'Can you tell me about the weather?' },
  { id: 3, message: 'Sure, it is currently sunny with a high of 75 degrees.' },
];

// Mock data for models
const models = ['Model 1', 'Model 2', 'Model 3'];

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'chat-app';
  selectedModel = models[0];
  message = '';
  chat = chatHistory;

  constructor(private http: HttpClient) {}

  sendMessage() {
    this.http.post('https://your-chat-service.com/api', {
      model: this.selectedModel,
      prompt: this.message
    }).subscribe(response => {
      this.chat.push({ id: Date.now(), message: response['message'] });
      this.message = '';
    }, error => {
      console.error(error);
    });
  }
}
