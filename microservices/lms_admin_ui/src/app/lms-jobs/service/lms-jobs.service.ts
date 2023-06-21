import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class JobsService {

  constructor(private http: HttpClient) { }

  getJobsList(skip: any, limit: any) {
    return this.http.get(`${environment.apiurl}lms-jobs?skip=${skip}&limit=${limit}`)
  }

}
