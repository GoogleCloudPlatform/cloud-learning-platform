import { CreateCourseTemplateModalComponent } from './create-course-template-modal/create-course-template-modal.component';
import { Component, OnInit,Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CreateCohortModalComponent } from './create-cohort-modal/create-cohort-modal.component';
import { HomeService } from './service/home.service';
import { environment } from 'src/environments/environment';
import { PageEvent } from '@angular/material/paginator';

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
  sectionList: any[]
  courseTemplateList: any[]
  courseTemplateLoader: boolean = true
  cohortLoader: boolean = true
  sectionLoader: boolean = true
  searchCohortTerm: string
  searchCourseTemplate: string
  searchSection: string
  pageEvent: PageEvent;

  cohortSkip: number = 0
  cohortLimit: number = 10
  cohortPageSize: number = 10

  courseTemplateSkip: number = 0
  courseTemplateLimit: number = 10
  courseTemplatePageSize: number = 10

  sectionSkip: number = 0
  sectionLimit: number = 10
  sectionPageSize: number = 10
  constructor(public dialog: MatDialog, public _HomeService: HomeService) {
  }

  ngOnInit(): void {
    this.getCohortList()
    this.getCourseTemplateList()
    this.getAllSectionsList()
  }
  handleCohortPageEvent(e: PageEvent) {
    this.pageEvent = e;
    console.log(this.pageEvent)

    if (this.pageEvent.pageSize != this.cohortPageSize) {
      this.cohortSkip = 0
      this.cohortLimit = this.pageEvent.pageSize
      this.cohortPageSize = this.pageEvent.pageSize
    }
    else {

      if (this.pageEvent.pageIndex > this.pageEvent.previousPageIndex) {
        this.cohortSkip = this.cohortLimit
        this.cohortLimit = this.cohortLimit + this.pageEvent.pageSize
      }
      else if (this.pageEvent.previousPageIndex > this.pageEvent.pageIndex) {
        this.cohortSkip = this.cohortSkip - this.pageEvent.pageSize
        this.cohortLimit = this.cohortLimit - this.pageEvent.pageSize
      }
    }
    console.log("skip ", this.cohortSkip, 'limit ', this.cohortLimit)
    this.getCohortList()
  }


  handleCourseTemplatePageEvent(e: PageEvent) {
    this.pageEvent = e;
    console.log(this.pageEvent)

    if (this.pageEvent.pageSize != this.courseTemplatePageSize) {
      this.courseTemplateSkip = 0
      this.courseTemplateLimit = this.pageEvent.pageSize
      this.courseTemplatePageSize = this.pageEvent.pageSize
    }
    else {

      if (this.pageEvent.pageIndex > this.pageEvent.previousPageIndex) {
        this.courseTemplateSkip = this.courseTemplateLimit
        this.courseTemplateLimit = this.courseTemplateLimit + this.pageEvent.pageSize
      }
      else if (this.pageEvent.previousPageIndex > this.pageEvent.pageIndex) {
        this.courseTemplateSkip = this.courseTemplateSkip - this.pageEvent.pageSize
        this.courseTemplateLimit = this.courseTemplateLimit - this.pageEvent.pageSize
      }
    }
    console.log("skip ", this.courseTemplateSkip, 'limit ', this.courseTemplateLimit)
    this.getCourseTemplateList()
  }


  handleSectionPageEvent(e: PageEvent) {
    this.pageEvent = e;
    console.log(this.pageEvent)

    if (this.pageEvent.pageSize != this.sectionPageSize) {
      this.sectionSkip = 0
      this.sectionLimit = this.pageEvent.pageSize
      this.sectionPageSize = this.pageEvent.pageSize
    }
    else {

      if (this.pageEvent.pageIndex > this.pageEvent.previousPageIndex) {
        this.sectionSkip = this.sectionLimit
        this.sectionLimit = this.sectionLimit + this.pageEvent.pageSize
      }
      else if (this.pageEvent.previousPageIndex > this.pageEvent.pageIndex) {
        this.sectionSkip = this.sectionSkip - this.pageEvent.pageSize
        this.sectionLimit = this.sectionLimit - this.pageEvent.pageSize
      }
    }
    console.log("skip ", this.sectionSkip, 'limit ', this.sectionLimit)
    this.getAllSectionsList()
  }


  getCourseTemplateList() {
    this.courseTemplateLoader = true
    this.courseTemplateList = []
    this._HomeService.getCourseTemplateList(this.courseTemplateSkip, this.courseTemplateLimit).subscribe((res: any) => {
      if (res.success == true) {
        this.courseTemplateList = res.course_template_list
        this.courseTemplateLoader = false
      }
    })
  }

  getCohortList() {
    this.cohortLoader = true
    this.cohortList = []
    this._HomeService.getCohortList(this.cohortSkip, this.cohortLimit).subscribe((res: any) => {
      if (res.success == true) {
        this.cohortList = res.cohort_list
        this.cohortLoader = false
      }
    })
  }

  getAllSectionsList() {
    this.sectionLoader = true
    this.sectionList = []
    this._HomeService.getAllSectionList(this.sectionSkip, this.sectionLimit).subscribe((res: any) => {
      if (res.success == true) {
        this.sectionList = res.data
        this.sectionLoader = false
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

@Component({
  selector: 'success-overview-dialog',
  templateUrl: 'success-overview-dialog.html',
})
export class SuccessOverviewDialog {
  constructor(
    public dialogRef: MatDialogRef<SuccessOverviewDialog>,
    @Inject(MAT_DIALOG_DATA) public successDialogData: any
  ) { }

  close(): void {
    this.dialogRef.close({ data: 'closed' });
  }
}

@Component({
  selector: 'course-template-details-dialog',
  templateUrl: 'course-template-details-dialog.html',
})
export class CourseTemplateDetailsDialog {
  constructor(
    public dialogRef: MatDialogRef<CourseTemplateDetailsDialog>,
    @Inject(MAT_DIALOG_DATA) public CourseTemplateDetailsDialogData: any
  ) {
    console.log('dialog data',CourseTemplateDetailsDialogData)
   }

  close(): void {
    this.dialogRef.close({ data: 'closed' });
  }
}