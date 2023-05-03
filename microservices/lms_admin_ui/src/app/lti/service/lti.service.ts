import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LtiService {

  constructor(private http: HttpClient) { }

  getToolData(id: string) {
    return this.http.get(`${environment.ltiUrl}tool/${id}`)
  }

  deleteTool(id: string) {
    return this.http.delete(`${environment.ltiUrl}tool/${id}`)
  }

  getToolsList() {
    return this.http.get(`${environment.ltiUrl}tools`)
  }

  postTool(data: object) {
    return this.http.post(`${environment.ltiUrl}tool`, data)
  }

  updateTool(id: string, data: object) {
    return this.http.put(`${environment.ltiUrl}tool/${id}`, data)
  }

}
