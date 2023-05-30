import { Component, OnInit, ViewChild, Inject,OnDestroy } from '@angular/core';
import { Location } from '@angular/common';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { MatSort, Sort } from '@angular/material/sort';
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CreateSectionComponent } from '../create-section/create-section.component';
import { HomeService } from '../service/home.service';
import { Router, NavigationStart, NavigationEnd, Event as NavigationEvent } from '@angular/router';
import { InviteStudentModalComponent } from '../invite-student-modal/invite-student-modal.component';
import { Subscription } from 'rxjs';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { CreateAssignmentComponent } from 'src/app/lti/create-assignment/create-assignment.component';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';

interface LooseObject {
  [key: string]: any
}

export interface staff {
  name: string;
  email: string;
  role: string;
  status:string;
}

export interface student {
  first_name: string;
  last_name: string;
  email: string;
  created_time: string;
}

export interface coursework {
  courseId: string,
      courseWorkId: string,
      title: string,
      state: string,
      creationTime: string,
      materials: [],
      status:string
}

export interface ltiAssignment {
  assignmentId: string,
  title: string,
  startDate: string,
  endDate: string,
  dueDate: string,
}

@Component({
  selector: 'app-section',
  templateUrl: './section.component.html',
  styleUrls: ['./section.component.scss']
})
export class SectionComponent implements OnInit,OnDestroy {
  selectedSection: any
  displayedColumns: string[] = ['name','email','role','status','action'];
  studentDisplayedColumns: string[] = ['first name', 'last name', 'email', 'created time','status','action'];
  courseworkDisplayColumns: string[] = ['title', 'state', 'created time','action']
  ltiAssignmentsDisplayedColumns: string[] = ["id", "lti_assignment_title", "start_date", "end_date", "due_date", "action"];
  teacherTableData: staff[] = []
  studentTableData: student[] = []
  courseworkTable: coursework[] = []
  ltiAssignmentsTableData: ltiAssignment[] = []
  // dataSource = new MatTableDataSource(this.tableData);

  cohortDetails: any
  courseTemplateDetails: any
  sectionDetails: any[] = []
  loadCard: boolean = false
  loadSection: boolean = false
  studentTableLoader:boolean=true
  teacherTableLoader:boolean=true
  courseworkTableLoader:boolean=true
  ltiAssignmentTableLoader:boolean=true
  getStudentListSub:Subscription
  getTeacherListSub:Subscription
  importGradesSub:Subscription
  disableCourseworkAction:boolean=false
  constructor(private _liveAnnouncer: LiveAnnouncer, private _snackBar: MatSnackBar, public dialog: MatDialog, public _HomeService: HomeService, 
    public router: Router, private _location: Location) { }
  @ViewChild(MatSort) sort: MatSort;


  ngOnInit(): void {
    let id
    console.log(this.router.url)
    id = this.router.url.split('/')[2]
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
        if (location.pathname.split('/' )[3]) {
          console.log('if router url split',this.router.url.split('/'))
          this.selectedSection = this.sectionDetails.find(o => o.id == location.pathname.split('/')[3])
          console.log('selected sec', this.selectedSection )
        }
        else {
          this.selectedSection = this.sectionDetails[0]
        }
        this.createTableData()
      }
      this.loadSection = false
      // console.log('section', this.sectionDetails)
    })
  }
  
  getCourseworkDetails(){
    this.courseworkTableLoader=true
    this._HomeService.getCourseworkDetails(this.selectedSection.id).subscribe((res:any)=>{
      this.transformCourseworkTableData(res.data)
      this.courseworkTableLoader=false
    },
    (err:any)=>{
      this.courseworkTableLoader=false
    })
  }
  
  getLtiAssignmentsDetails(){
    this.ltiAssignmentTableLoader=true
    console.log("URL for lti ",this._HomeService.getLtiAssignments)
    this._HomeService.getLtiAssignments(this.selectedSection.id).subscribe((res:any)=>{
      console.log("Resi;t ->",res.data)
      this.ltiAssignmentsTableData = res.data
      console.log("ltiAssignmentData ->",this.ltiAssignmentsTableData)
      this.ltiAssignmentTableLoader=false
    },
    (err:any)=>{
      this.ltiAssignmentTableLoader=false
    })
  }


transformCourseworkTableData(data:any){
  this.courseworkTable=[]
  for (let x of data){
    x['status'] = 'import'
    this.courseworkTable.push(x)
  }
  console.log('coursework',this.courseworkTable)
}

  openClassroom() {
    window.open(this.selectedSection.classroom_url
      , '_blank');
  }
  getSectionStudents() {
    this.studentTableLoader = true
    if(this.getStudentListSub){
      this.getStudentListSub.unsubscribe();
    }
    this.getStudentListSub=this._HomeService.getStudentsInSection(this.selectedSection.id).subscribe((res: any) => {
      this.studentTableData = []
      this.studentTableData = res.data
      console.log('student data', this.studentTableData)
      this.studentTableLoader = false
    },
    (err:any)=>{
      this.studentTableLoader = false
    }
    )
  }

  getSectionTeachers(){
    this.teacherTableLoader = true
    if(this.getTeacherListSub){
      this.getTeacherListSub.unsubscribe();
    }
    this.getTeacherListSub=this._HomeService.getTeachersInSection(this.selectedSection.id).subscribe((res: any) => {
      this.teacherTableData = []
      for (let x of res.data) {
      let staffObj: staff = { name: '', email: '', role: '', status:'' }
      staffObj.name = x.first_name+' '+x.last_name
      staffObj.email = x.email
      staffObj.role = 'Teaching Staff'
      staffObj.status = x.status
      this.teacherTableData.push(staffObj)
    }

      console.log('teacher data', this.teacherTableData)
      this.teacherTableLoader = false
    },
    (err:any)=>{
      this.teacherTableLoader = false
    }
    )
  }

  updateUrl(url: string) {
    console.log('path',location.pathname)
    let pathArr = location.pathname.split('/')
    if(pathArr.length == 4){
      pathArr[3] = url
    }
    else{
      pathArr.push(url)
    }
    console.log(pathArr.toString().replace(/,/g,'/'))
    this._location.go(pathArr.toString().replace(/,/g,'/'))
  }

  createTableData() {
    console.log('selected sec', this.selectedSection)
    if(this.importGradesSub){
      this.importGradesSub.unsubscribe();
    }
    this.disableCourseworkAction=false
    this.updateUrl(this.selectedSection.id)
    this.getSectionStudents()
    this.getSectionTeachers()
    this.getCourseworkDetails()
    this.getLtiAssignmentsDetails()

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
    // tempObj['teachers'] = []
    // for (let x of this.selectedSection.teachers) {
    //   if (x != this.courseTemplateDetails.admin && x != this.courseTemplateDetails.instructional_designer) {
    //     tempObj['teachers'].push(x)
    //   }
    // }

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

  openDeleteDialog(firstName: any, lastName: any, userId: any) {
    let deleteDialogData: LooseObject = {}
    deleteDialogData['first_name'] = firstName
    deleteDialogData['last_name'] = lastName
    deleteDialogData['section'] = this.selectedSection.section
    deleteDialogData['user_id'] = userId
    deleteDialogData['section_id'] = this.selectedSection.id
    deleteDialogData['type'] = 'student'
    const dialogRef = this.dialog.open(DeleteOverviewDialog, {
      width: '500px',
      data: deleteDialogData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getSectionStudents()
      }
    });
  }

  openTeacherDeleteDialog(name:any,email:any){
    let deleteDialogData: LooseObject = {}
    deleteDialogData['name'] = name
    deleteDialogData['email'] = email
    deleteDialogData['section_name'] = this.selectedSection.section
    deleteDialogData['id'] = this.selectedSection.id
    deleteDialogData['type'] = 'teacher'
    const dialogRef = this.dialog.open(DeleteOverviewDialog, {
      width: '500px',
      data: deleteDialogData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getSectionTeachers()
      }
    });
  }

  openInviteStudentDialog(){
    console.log('selected sec',this.selectedSection)
    let tempObj: LooseObject = {}
    tempObj['cohort_name'] = this.cohortDetails.name
    tempObj['section'] = this.selectedSection.section
    tempObj['section_id'] = this.selectedSection.id

    let inviteStudentModalData: LooseObject = {}
    inviteStudentModalData['mode'] = 'Section'
    inviteStudentModalData['init_data'] = tempObj
    inviteStudentModalData['extra_data'] = ''
    const dialogRef = this.dialog.open(InviteStudentModalComponent, {
      width: '500px',
      data: inviteStudentModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == 'success') {
        this.getSectionStudents()
      }
    });
  }

  openUpdateLtiAssignmentDialog(id, data) {
    let sectionId = this.selectedSection.id
    let ltiModalData = {}
    ltiModalData['mode'] = 'Update'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { sectionId, assignment: data }

    const dialogRef = this.dialog.open(CreateAssignmentComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
      if (result?.data == "success") {
        this.getLtiAssignmentsDetails()
      }
    });
  }

  openDeleteLtiAssignmentDialog(id, name) {
    let courseTemplateId = this.router.url.split('/')[this.router.url.split('/').length - 1]
    const dialogRef = this.dialog.open(DeleteSectionLtiDialog, {
      width: '500px',
      data: { id, name }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
        this.getLtiAssignmentsDetails()
      }
      console.log("result", result)
    });
    console.log(id)
  }

  openViewLtiAssignmentDialog(id, data): void {
    console.log("id", id)
    let ltiModalData = {}
    ltiModalData['mode'] = 'View'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { id, ...data }

    const dialogRef = this.dialog.open(ViewSectionLtiAssignmentDialog, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
    });
  }

  openAddLtiAssignmentDialog() {
    let ltiModalData = {}
    let sectionId = this.selectedSection.id
    ltiModalData['mode'] = 'Create'
    ltiModalData['page'] = 'section'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { "contextId": sectionId}

    const dialogRef = this.dialog.open(CreateAssignmentComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
      if (result?.data == "success") {
        this.getLtiAssignmentsDetails()
      }
    });
  }

  checkIfActive(start: string, end: string): boolean {
    let startDate = Date.parse(start)
    let endDate = Date.parse(end)
    let d = Date.now()
    if (d.valueOf() >= startDate.valueOf() && d.valueOf() <= endDate.valueOf()) {
      return true
    }
    else {
      return false
    }

  }
  ifUpcoming(start: string): boolean {
    let startDate = Date.parse(start)
    let d = Date.now()
    if (d.valueOf() < startDate.valueOf()) {
      return true
    }
    else {
      return false
    }
  }
  callGradeImport(rowNumber:any,courseworkId:string){
    console.log("row num", rowNumber)
    this.disableCourseworkAction=true
    this.courseworkTable[rowNumber]['status'] = 'loading'
    this.importGradesSub = this._HomeService.gradeImport(this.selectedSection.id,courseworkId).subscribe((res:any)=>{
  this.courseworkTable[rowNumber]['status'] = 'import_done'
  this.disableCourseworkAction=false
  this.openSuccessSnackBar(res.message,'Close')
},(err:any)=>{
  this.courseworkTable[rowNumber]['status'] = 'import_error'
  this.disableCourseworkAction=false
})
  }
  checkMaterialsArray(materials:any[]){
    let status:boolean=false
    for (let x of materials){
      if('form' in x){
        status = true
        break
      }
    }
    return status
  }

  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['green-snackbar'],
    });
  }
  openAddTeacherDialog(){
    let sectionTemp:LooseObject={}
    sectionTemp['name'] = this.selectedSection.section
    sectionTemp['id'] = this.selectedSection.id
    console.log('data sent',sectionTemp)
    const dialogRef = this.dialog.open(addTeacherDialog, {
      width: '500px',
      data: sectionTemp
    });
  }
  getStatusName(status:any){
    return status.replace(/_/g,' ')
  }
  getChipClass(status:any){
return 'section-'+status+'-chip'
  }
  onChipClick(){
    console.log('chip click')
  }

  ngOnDestroy(): void {
    if(this.getStudentListSub){
      this.getStudentListSub.unsubscribe();
    }
    if(this.importGradesSub){
      this.importGradesSub.unsubscribe();
    }
  }

}


@Component({
  selector: 'add-teacher-dialog',
  templateUrl: 'add-teacher-dialog.html',
})
export class addTeacherDialog {
  addTeacherForm:UntypedFormGroup
  showProgressSpinner:boolean=false
  constructor(
    public dialogRef: MatDialogRef<addTeacherDialog>,
    @Inject(MAT_DIALOG_DATA) public addTeacherDialogData: any,
    private fb: UntypedFormBuilder,
    public homeService: HomeService,
    private _snackBar: MatSnackBar
  ) 
  {
  }
  ngOnInit():void{
    this.addTeacherForm = this.fb.group({
      email: this.fb.control('', [Validators.required, Validators.email])
    })

  }

  addTeacher(){
    console.log(this.addTeacherForm.value)
    this.showProgressSpinner=true
this.homeService.addTeacher(this.addTeacherDialogData.id,this.addTeacherForm.value).subscribe((res:any)=>{
this.showProgressSpinner=false
if(res.success == true){
this.openSuccessSnackBar(res.message,'Success')
}
this.addTeacherForm.reset()
},(err:any)=>{
  this.showProgressSpinner=false
})
  }

  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['green-snackbar'],
    });
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'view-lti-assignment-dialog',
  templateUrl: 'view-lti-assignment-dialog.html',
})
export class ViewSectionLtiAssignmentDialog {
  ltiAssignmentData: any;
  objectKeys = Object.keys
  constructor(
    public dialogRef: MatDialogRef<ViewSectionLtiAssignmentDialog>,
    @Inject(MAT_DIALOG_DATA) public viewDialogData: any, public homeService: HomeService
  ) {
    this.ltiAssignmentData = viewDialogData.extra_data
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'delete-overview-dialog',
  templateUrl: 'delete-overview-dialog.html',
})
export class DeleteOverviewDialog {
  constructor(
    public dialogRef: MatDialogRef<DeleteOverviewDialog>,
    @Inject(MAT_DIALOG_DATA) public deleteDialogData: any, public _HomeService: HomeService
  ) { }
  
  delete(){
    if(this.deleteDialogData.type == 'student'){
      this._HomeService.deleteStudent(this.deleteDialogData.user_id, this.deleteDialogData.section_id).subscribe((res: any) => {
        if (res.success == true) {
          this.dialogRef.close({ data: 'success' });
        }
      }) 
    }
    else{
      this._HomeService.deleteTeacher(this.deleteDialogData.id,this.deleteDialogData.email).subscribe((res:any)=>{
        if (res.success == true) {
          this.dialogRef.close({ data: 'success' });
        }
      }) 
    }
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'delete-lti-assignment-dialog',
  templateUrl: 'delete-lti-assignment-dialog.html',
})
export class DeleteSectionLtiDialog {
  constructor(
    public dialogRef: MatDialogRef<DeleteSectionLtiDialog>,
    @Inject(MAT_DIALOG_DATA) public deleteDialogData: any, public homeService: HomeService
  ) { }

  deleteAssignment() {
    this.homeService.deleteLtiAssignments(this.deleteDialogData.id).subscribe((res: any) => {
      if (res.success == true) {
        this.dialogRef.close({ data: 'success' });
      }
    })
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}