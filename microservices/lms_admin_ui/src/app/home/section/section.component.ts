import { Component, OnInit, ViewChild } from '@angular/core';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatSort, Sort } from '@angular/material/sort';
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CreateSectionComponent } from '../create-section/create-section.component';
import { HomeService } from '../service/home.service';
import { Router, NavigationStart, NavigationEnd, Event as NavigationEvent } from '@angular/router';

interface LooseObject {
  [key: string]: any
}

export interface staff {
  name: string;
  email: string;
  role: string;
}

@Component({
  selector: 'app-section',
  templateUrl: './section.component.html',
  styleUrls: ['./section.component.scss']
})
export class SectionComponent implements OnInit {
  selectedSection: any
  displayedColumns: string[] = ['name', 'email', 'role'];

  tableData: staff[] = []
  dataSource = new MatTableDataSource(this.tableData);

  cohortDetails: any
  courseTemplateDetails: any
  sectionDetails: any[] = []
  loadCard: boolean = false
  loadSection: boolean = false
  constructor(private _liveAnnouncer: LiveAnnouncer, public dialog: MatDialog, public _HomeService: HomeService, public router: Router) { }
  @ViewChild(MatSort) sort: MatSort;


  ngOnInit(): void {
    this.dataSource.sort = this.sort;
    let id
    console.log(this.router.url)
    id = this.router.url.split('/')[3]
    this.getCohortDetails(id)


  }

  getCohortDetails(id: any) {
    this.loadCard = true
    this.loadSection = true
    this._HomeService.getCohort(id).subscribe((res: any) => {
      this.cohortDetails = res
      console.log('cohort details', this.cohortDetails)
      this.getCourseTemplateDetails(res.course_template.split('/')[1])
    })
  }
  getCourseTemplateDetails(id: any) {
    this._HomeService.getCourseTemplate(id).subscribe((res: any) => {
      this.courseTemplateDetails = res
      this.loadCard = false
      console.log('course template', this.courseTemplateDetails)
      this.getSectionList(this.cohortDetails.id)
    })
  }

  getSectionList(cohortid: any) {
    this.loadSection = true
    this._HomeService.getSectionList(cohortid).subscribe((res: any) => {
      this.sectionDetails = res.data
      if (this.sectionDetails.length > 0) {
        this.selectedSection = this.sectionDetails[0]
        this.createTableData()
      }
      this.loadSection = false
      // console.log('section', this.sectionDetails)
    })
  }
  createTableData() {
    console.log('selected sec', this.selectedSection)
    this.tableData = []
    for (let x of this.selectedSection.teachers_list) {
      let staffObj: staff = { name: '', email: '', role: '' }
      staffObj.name = 'TBD'
      staffObj.email = x
      if (x == this.courseTemplateDetails.admin) {
        staffObj.role = 'Admin'
      }
      else if (x == this.courseTemplateDetails.instructional_designer) {
        staffObj.role = 'Instructional Designer'
      }
      else {
        staffObj.role = 'Teaching Staff'
      }
      this.tableData.push(staffObj)
    }
    console.log('table data', this.tableData)

  }

  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }

  openCreateSectionDialog(): void {
    let tempObj: LooseObject = {}
    tempObj['cohort_name'] = this.cohortDetails.name
    tempObj['course_template_name'] = this.courseTemplateDetails.name
    tempObj['cohort_id'] = this.cohortDetails.id
    tempObj['course_template_id'] = this.courseTemplateDetails.id
    tempObj['instructional_desiner'] = this.courseTemplateDetails.instructional_designer
    tempObj['admin'] = this.courseTemplateDetails.admin


    let sectionModalData: LooseObject = {}
    sectionModalData['mode'] = 'Create'
    sectionModalData['init_data'] = ''
    sectionModalData['extra_data'] = tempObj

    const dialogRef = this.dialog.open(CreateSectionComponent, {
      width: '500px',
      data: sectionModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getSectionList(this.cohortDetails.id)
      }
    });
  }

  openEditSelectionDialog(): void {
    let tempObj: LooseObject = {}
    tempObj['cohort_name'] = this.cohortDetails.name
    tempObj['course_template_name'] = this.courseTemplateDetails.name
    tempObj['cohort_id'] = this.cohortDetails.id
    tempObj['course_template_id'] = this.courseTemplateDetails.id
    tempObj['instructional_desiner'] = this.courseTemplateDetails.instructional_designer
    tempObj['admin'] = this.courseTemplateDetails.admin
    tempObj['section_id'] = this.selectedSection.id
    tempObj['section'] = this.selectedSection.section
    tempObj['description'] = this.selectedSection.description
    tempObj['classroom_id'] = this.selectedSection.classroom_id
    tempObj['teachers'] = []
    for (let x of this.selectedSection.teachers) {
      if (x != this.courseTemplateDetails.admin && x != this.courseTemplateDetails.instructional_designer) {
        tempObj['teachers'].push(x)
      }
    }

    let sectionModalData: LooseObject = {}
    sectionModalData['mode'] = 'Edit'
    sectionModalData['init_data'] = tempObj
    sectionModalData['extra_data'] = ''

    const dialogRef = this.dialog.open(CreateSectionComponent, {
      width: '500px',
      data: sectionModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getSectionList(this.cohortDetails.id)
      }
    });
  }

}
