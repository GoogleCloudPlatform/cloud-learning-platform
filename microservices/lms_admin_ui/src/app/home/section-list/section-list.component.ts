import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-section-list',
  templateUrl: './section-list.component.html',
  styleUrls: ['./section-list.component.scss']
})
export class SectionListComponent implements OnInit {
  @Input() sectionList: any[]
  constructor(public router: Router) { }

  ngOnInit(): void {
  }
  reRout(cohortUrl: any) {
    this.router.navigate(['/home/' + cohortUrl.split('/')[1]])
  }
  openClassroom(link: any) {
    window.open(link
      , '_blank');
  }
}
