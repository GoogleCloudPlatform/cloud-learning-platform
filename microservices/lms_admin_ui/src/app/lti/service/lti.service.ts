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

  getContentItems(tool_id: string, context_id: string) {
    return this.http.get(`${environment.classroomShimUrl}context/${context_id}/content-items?tool_id=${tool_id}`)
  }

  postTool(data: object) {
    return this.http.post(`${environment.ltiUrl}tool`, data)
  }
  
  updateTool(id: string, data: object) {
    return this.http.put(`${environment.ltiUrl}tool/${id}`, data)
  }
  
  contentSelectionLaunch(tool_id: string, user_id: string, context_id: string, context_type: string) {
    return this.http.get(`${environment.ltiUrl}content-selection-launch-init?tool_id=${tool_id}&user_id=${user_id}&context_id=${context_id}&context_type=${context_type}`)
  }

  postContentItem(data: object) {
    return this.http.post(`${environment.ltiUrl}content-item`, data)
  }

}
