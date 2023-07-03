import { CreateCourseTemplateModalComponent } from './../create-course-template-modal/create-course-template-modal.component';
import { Component, OnInit, Input,Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CourseTemplateDetailsDialog } from '../home.component';
import { HomeService } from '../service/home.service';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';
import { Router } from '@angular/router';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-course-template',
  templateUrl: './course-template.component.html',
  styleUrls: ['./course-template.component.scss']
})
export class CourseTemplateComponent implements OnInit {
  apiCall:number = 0
  @Input() courseTemplateList
  constructor(public dialog: MatDialog, public router: Router,public _HomeService: HomeService) { 
    
  }
  selectedCourseTemplate: any
  ngOnInit(): void {
    console.log('list', this.courseTemplateList)
this.callToGetId()
  }

  callToGetId(){
    for(let x=0;x<this.courseTemplateList.length;x++){
      this._HomeService.getInstructionalDesigner(this.courseTemplateList[x].id).subscribe((res:any)=>{
        if(res.data.length > 0){
          this.courseTemplateList[x]['instructional_designer']=res.data
        }
        else{
          this.courseTemplateList[x]['instructional_designer']='null'
        }
        
})

}
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


  reRoute(courseTemplate: any) {
    this.router.navigate(['/home/course-template/' + courseTemplate.id])
  }


  setSelected(courseTemplate: any) {
    this.selectedCourseTemplate = courseTemplate
  }
  openEditCourseTemplate() {
    let courseTemplateModalData: LooseObject = {}
    courseTemplateModalData['mode'] = 'Edit'
    courseTemplateModalData['init_data'] = this.selectedCourseTemplate
    courseTemplateModalData['extra_data'] = ''
    const dialogRef = this.dialog.open(CreateCourseTemplateModalComponent, {
      width: '500px',
      data: courseTemplateModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(result)
      if (result.data == 'success') {
      }
    });
  }

  openClassroom(link: any) {
    window.open(link
      , '_blank');
  }

  openDetailsDialogue(data: any) {
    const CourseTemplateDetailsDialogRef = this.dialog.open(CourseTemplateDetailsDialog, {
      width: '600px',
      data: data
    });
  }
  openAddOrEditIdTemplate(){
    let idData: LooseObject = {}
    idData['course_template_name'] = this.selectedCourseTemplate.name
    idData['course_template_id'] = this.selectedCourseTemplate.id

    const dialogRef = this.dialog.open(AddOrEditCcourseTemplate, {
      width: '650px',
      data: idData
    });

    // dialogRef.afterClosed().subscribe(result => {
    //   if (result.data == 'success') {
    //     this.getSectionStudents()
    //   }
    // });
  }
  getInstructionalDesigner(course_template_id:string){
    // this._HomeService.getInstructionalDesigner(course_template_id).subscribe((res:any)=>{
    //   return res.data[0]['email']
    // })
    this.apiCall = this.apiCall+1
    console.log(course_template_id, this.apiCall)
    return course_template_id
  }

}

@Component({
  selector: 'add-or-edit-course-template-dialog',
  templateUrl: 'add-or-edit-course-template-dialog.html',
})
export class AddOrEditCcourseTemplate {
  addIdForm:UntypedFormGroup
  showProgressSpinner:boolean=false

  idTableLoader:boolean=true
  idTableData:any[]=[]
  idDisplayedColumns:string[]=['name','email','status','action']
  constructor(
    public dialogRef: MatDialogRef<AddOrEditCcourseTemplate>,
    @Inject(MAT_DIALOG_DATA) public idData: any, public _HomeService: HomeService,
    private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar
  ) { }

  ngOnInit():void{
    this.addIdForm = this.fb.group({
      email: this.fb.control('', [Validators.required, Validators.email])
    })
this.getInstructionalDesigner()
  }
  getInstructionalDesigner(){
    this.idTableLoader = true
    this._HomeService.getInstructionalDesigner(this.idData.course_template_id).subscribe((res:any)=>{
      this.idTableData = res.data
      this.idTableLoader = false
    })
  }

  addInstructionalDesigner() {
    this.showProgressSpinner=true
 this._HomeService.addInstructionalDesigner(this.idData.course_template_id,this.addIdForm.value).subscribe((res:any)=>{
this.showProgressSpinner=false
if(res.success == true){
  this.openSuccessSnackBar(res.message,'Success')
  this.getInstructionalDesigner()
}
 },(err:any)=>{
this.showProgressSpinner=false
 })
  }

  deleteInstructionalDesigner(email:string){
this._HomeService.deleteInstructionalDesigner(this.idData.course_template_id,email).subscribe((res:any)=>{
  if(res.success == true){
    this.openSuccessSnackBar(email+' Deleted','Success')
    this.getInstructionalDesigner()
  }
})
  }

  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 4000,
      panelClass: ['green-snackbar'],
    });
  }


  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}
