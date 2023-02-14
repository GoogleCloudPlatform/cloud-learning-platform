import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  constructor(private http: HttpClient) { }
  getCohortList(skip: any, limit: any) {
    return this.http.get(`${environment.apiurl}cohorts?skip=${skip}&limit=${limit}`)

  }
  getCourseTemplateList(skip: any, limit: any) {
    return this.http.get(`${environment.apiurl}course_templates?skip=${skip}&limit=${limit}`)

  }
  getAllSectionList(skip: any, limit: any) {
    return this.http.get(`${environment.apiurl}sections?skip=${skip}&limit=${limit}`)
  }
  editCourseTemplate(data: any, id: any) {
    return this.http.patch(`${environment.apiurl}course_templates/${id}`, data)
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
  editCohort(data: any, id: any) {
    return this.http.patch(`${environment.apiurl}cohorts/${id}`, data)
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
  editSection(data: any) {
    return this.http.patch(`${environment.apiurl}sections`, data)
  }
  getStudentsInSection(sectionId: any) {
    return this.http.get(`${environment.apiurl}sections/${sectionId}/students`)
  }
  deleteStudent(userId: any, sectionId: any) {
    return this.http.delete(`${environment.apiurl}/sections/${sectionId}/students/${userId}`)
  }
}
