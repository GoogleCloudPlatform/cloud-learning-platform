import { Component, OnInit } from '@angular/core';
import { HomeService } from '../service/home.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-single-template',
  templateUrl: './single-template.component.html',
  styleUrls: ['./single-template.component.scss']
})
export class SingleTemplateComponent implements OnInit{

  constructor(private router: Router,private homeService: HomeService){

  }

  ngOnInit(): void {
    let courseTemplateId = this.router.
    this.fetchDetails()
  }

  fetchDetails(id) {

  }

// fetch details of the course template
// add it to ui
// 
}
