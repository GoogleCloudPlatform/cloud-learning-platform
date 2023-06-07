import { Component, Inject, OnInit } from '@angular/core';
import { HomeService } from '../service/home.service';
import { Router } from '@angular/router';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { MatLegacyTableDataSource as MatTableDataSource } from '@angular/material/legacy-table'
import { MatSort } from '@angular/material/sort';
import { CreateAssignmentComponent } from 'src/app/lti/create-assignment/create-assignment.component';

@Component({
  selector: 'app-single-template',
  templateUrl: './single-template.component.html',
  styleUrls: ['./single-template.component.scss']
})
export class SingleTemplateComponent implements OnInit {

  courseTemplateDetails: any
  ltiAssignments = []
  loadCard = false
  loadTable = false
  dataSource = new MatTableDataSource(this.ltiAssignments);
  ltiAssignmentsDisplayedColumns: string[] = ["id", "lti_assignment_title", "start_date", "end_date", "due_date", "action"];
  instructionalDesignerList:string[]=[]

  constructor(private router: Router, private homeService: HomeService, public dialog: MatDialog) {

  }

  ngOnInit(): void {
    let courseTemplateId = this.router.url.split('/')[this.router.url.split('/').length - 1]
    this.fetchDetails(courseTemplateId)
    this.fetchLtiAssignments(courseTemplateId)
    this.getInstructionalDesignerDetails(courseTemplateId)

  }

  getInstructionalDesignerDetails(id:any){
    this.homeService.getInstructionalDesigner(id).subscribe((res:any)=>{
this.instructionalDesignerList=res.data
    })
  }
  getIdTotal(id:any){
    return '+'+(id.length-1)
    }
    checkIfBadgeHidden(id:any){

      if(id.length < 2){
        return true
      }
      else{
        return false
      }
    }
    getMattooltipText(arr:any){
      if(arr.length == 1){
        return arr[0]['email']
      }
      else{
        let text=''
        for(let x of arr){
          text = text+x['email']+' , '
        }
        return text
      }
    }

  fetchDetails(contextId) {
    this.homeService.getCourseTemplate(contextId).subscribe(
      (res: any) => {
        this.loadCard = true
        this.courseTemplateDetails = res
        console.log('course template', this.courseTemplateDetails)
      }
    )
  }

  fetchLtiAssignments(contextId) {
    this.homeService.getLtiAssignments(contextId).subscribe(
      (res: any) => {
        this.loadTable = true
        this.ltiAssignments = res.data
        console.log('this.ltiAssignments', this.ltiAssignments)
      }
    )
  }

  openAddAssignmentDialog() {
    let courseTemplateId = this.router.url.split('/')[this.router.url.split('/').length - 1]
    let ltiModalData = {}
    ltiModalData['mode'] = 'Create'
    ltiModalData['page'] = 'course_template'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { "contextId": courseTemplateId }

    const dialogRef = this.dialog.open(CreateAssignmentComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });
    
    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
      if (result?.data == "success") {
        this.fetchLtiAssignments(courseTemplateId)
      }
    });
  }

  openUpdateDialog(id, data) {
    let courseTemplateId = this.router.url.split('/')[this.router.url.split('/').length - 1]
    let ltiModalData = {}
    ltiModalData['mode'] = 'Update'
    ltiModalData['page'] = 'course_template'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { "contextId": courseTemplateId, assignment: data }

    const dialogRef = this.dialog.open(CreateAssignmentComponent, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
      if (result?.data == "success") {
        this.fetchLtiAssignments(courseTemplateId)
      }
    });
  }

  openDeleteDialog(id, name) {
    let courseTemplateId = this.router.url.split('/')[this.router.url.split('/').length - 1]
    const dialogRef = this.dialog.open(DeleteLtiDialog, {
      width: '500px',
      data: { id, name }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.data == "success") {
        this.fetchLtiAssignments(courseTemplateId)
      }
      console.log("result", result)
    });
    console.log(id)
  }

  openViewAssignmentsDialog(id, data): void {
    console.log("id", id)
    let ltiModalData = {}
    ltiModalData['mode'] = 'View'
    ltiModalData['init_data'] = ''
    ltiModalData['extra_data'] = { id, ...data }

    const dialogRef = this.dialog.open(ViewLtiAssignmentDialog, {
      width: '80vw',
      maxWidth: '750px',
      maxHeight: "90vh",
      data: ltiModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log("result", result)
    });
  }

}

@Component({
  selector: 'view-lti-assignment-dialog',
  templateUrl: 'view-lti-assignment-dialog.html',
})
export class ViewLtiAssignmentDialog {
  ltiAssignmentData: any;
  objectKeys = Object.keys
  constructor(
    public dialogRef: MatDialogRef<ViewLtiAssignmentDialog>,
    @Inject(MAT_DIALOG_DATA) public viewDialogData: any, public homeService: HomeService
  ) {
    this.ltiAssignmentData = viewDialogData.extra_data
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}

@Component({
  selector: 'delete-lti-assignment-dialog',
  templateUrl: 'delete-lti-assignment-dialog.html',
})
export class DeleteLtiDialog {
  constructor(
    public dialogRef: MatDialogRef<DeleteLtiDialog>,
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