import { CreateCourseTemplateModalComponent } from './create-course-template-modal/create-course-template-modal.component';
import { Component, OnInit } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CreateCohortModalComponent } from './create-cohort-modal/create-cohort-modal.component';
import { HomeService } from './service/home.service';
import { environment } from 'src/environments/environment';

interface LooseObject {
  [key: string]: any
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  searchText: string = '';
  cohortList: any[]
  courseTemplateList: any[]
  courseTemplateLoader: boolean = true
  cohortLoader: boolean = true
  searchCohortTerm: string
  searchCourseTemplate: string
  constructor(public dialog: MatDialog, public _HomeService: HomeService) {
    // console.log('env var', environment.apiurl);
  }

  ngOnInit(): void {
    this.getCohortList()
    this.getCourseTemplateList()
  }
  getCourseTemplateList() {
    this.courseTemplateLoader = true
    this.courseTemplateList = []
    this._HomeService.getCourseTemplateList().subscribe((res: any) => {
      if (res.success == true) {
        this.courseTemplateList = res.course_template_list
        this.courseTemplateLoader = false
      }
    })
  }
  getCohortList() {
    this.cohortLoader = true
    this.cohortList = []
    this._HomeService.getCohortList().subscribe((res: any) => {
      if (res.success == true) {
        this.cohortList = res.cohort_list
        this.cohortLoader = false
      }
    })
  }


  openDialog(): void {
    let cohortModalData: LooseObject = {}
    cohortModalData['mode'] = 'Create'
    cohortModalData['init_data'] = ''
    cohortModalData['extra_data'] = this.courseTemplateList
    const dialogRef = this.dialog.open(CreateCohortModalComponent, {
      width: '500px',
      data: cohortModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getCohortList()
      }
    });
  }

  openCourseTemplateDialog(): void {
    let courseTemplateModalData: LooseObject = {}
    courseTemplateModalData['mode'] = 'Create'
    courseTemplateModalData['init_data'] = ''
    courseTemplateModalData['extra_data'] = ''
    const dialogRef = this.dialog.open(CreateCourseTemplateModalComponent, {
      width: '500px',
      data: courseTemplateModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(result)
      if (result.data == 'success') {
        this.getCourseTemplateList()
      }
    });
  }


}
