import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-course-template',
  templateUrl: './course-template.component.html',
  styleUrls: ['./course-template.component.scss']
})
export class CourseTemplateComponent implements OnInit {
  @Input() courseTemplateList: any[]
  constructor() { }

  ngOnInit(): void {
  }

}
