import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  constructor(private http: HttpClient) { }
  getCohortList() {
    return this.http.get(`${environment.apiurl}cohorts`)

  }
  getCourseTemplateList() {
    return this.http.get(`${environment.apiurl}course_templates`)

  }
  createCourseTemplate(data: any) {
    return this.http.post(`${environment.apiurl}course_templates`, data)
  }
  createCohort(data: any) {
    return this.http.post(`${environment.apiurl}cohorts`, data)
  }
  getCohort(data: any) {
    return this.http.get(`${environment.apiurl}cohorts/${data}`)
  }
  getCourseTemplate(data: any) {
    return this.http.get(`${environment.apiurl}course_templates/${data}`)
  }
  getSectionList(data: any) {
    return this.http.get(`${environment.apiurl}cohorts/${data}/sections`)
  }
  createSection(data: any) {
    return this.http.post(`${environment.apiurl}sections`, data)
  }
}
