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
  reRout(cohortUrl: any, sectionId: any) {
    this.router.navigate(['/home/' + cohortUrl.split('/')[1] + '/' + sectionId])
  }
  openClassroom(link: any) {
    window.open(link
      , '_blank');
  }
  getStatusName(status:any){
    return status.replace(/_/g,' ')
  }
  getChipClass(status:any){
return 'section-'+status+'-chip'
  }
  onChipClick(){
  }
}
