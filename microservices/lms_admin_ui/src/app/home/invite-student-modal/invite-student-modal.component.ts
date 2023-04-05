import { Component, OnInit, Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HomeService } from '../service/home.service';
import { SuccessOverviewDialog } from '../home.component';

@Component({
  selector: 'app-invite-student-modal',
  templateUrl: './invite-student-modal.component.html',
  styleUrls: ['./invite-student-modal.component.scss']
})
export class InviteStudentModalComponent implements OnInit{
  inviteStudentForm: UntypedFormGroup
  showProgressSpinner: boolean = false
  constructor(public dialog: MatDialog,public dialogRef: MatDialogRef<InviteStudentModalComponent>, private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService, @Inject(MAT_DIALOG_DATA) public InviteStudentModalData: any) { }
    ngOnInit(): void {
      console.log("data ", this.InviteStudentModalData)
      if (this.InviteStudentModalData.mode == 'Cohort') {
        this.inviteStudentForm = this.fb.group({
          cohortName: this.fb.control({ value: this.InviteStudentModalData.init_data.name, disabled: true }, [Validators.required]),
          studentEmail: this.fb.control('', [Validators.required, Validators.email]),
        });
      }
      else {
        this.inviteStudentForm = this.fb.group({
          cohortName: this.fb.control({ value: this.InviteStudentModalData.init_data.cohort_name, disabled: true }, [Validators.required]),
          sectionName: this.fb.control({ value: this.InviteStudentModalData.init_data.section, disabled: true }, [Validators.required]),
          studentEmail: this.fb.control('', [Validators.required, Validators.email]),
        });
      }
    }
  
    inviteStudent():void{
      console.log(this.inviteStudentForm.value.studentEmail)
      if (this.InviteStudentModalData.mode == 'Cohort'){
        this.showProgressSpinner=true
this._HomeService.inviteInCohort(this.InviteStudentModalData.init_data.id,this.inviteStudentForm.value.studentEmail).subscribe((res:any)=>{
  if (res.success == true) {
    this.dialogRef.close({ data: 'success' });

    const successOverviewDialogRef = this.dialog.open(SuccessOverviewDialog, {
      width: '500px',
      data: "Student invited successfully! Please ask student to check email"
    });
  }
this.showProgressSpinner=false
},error=>{
  if(error.status == 409){
    this.inviteStudentForm.controls['studentEmail'].setErrors({ 'user present': true})
  }
  this.showProgressSpinner=false
})
}
else{
console.log(this.InviteStudentModalData)
  this.showProgressSpinner=true
  this._HomeService.inviteInSection(this.InviteStudentModalData.init_data.section_id,this.inviteStudentForm.value.studentEmail).subscribe((res:any)=>{
    if (res.success == true) {
      this.dialogRef.close({ data: 'success' });
  
      const successOverviewDialogRef = this.dialog.open(SuccessOverviewDialog, {
        width: '500px',
        data: "Student invited successfully! Please ask student to check email"
      });
    }
  this.showProgressSpinner=false
  },error=>{
    if(error.status == 409){
      this.inviteStudentForm.controls['studentEmail'].setErrors({ 'user present': true})
    }
    this.showProgressSpinner=false
  })


}
    }

    getErrorMessage() {
      if (this.inviteStudentForm.controls['studentEmail'].hasError('required')) {
        return 'You must enter a value';
      }else if(this.inviteStudentForm.controls['studentEmail'].hasError('user present')){
        return 'User already exists';
      }
      else if(this.inviteStudentForm.controls['studentEmail'].hasError('email')){
        return 'Not a valid email';
      }
      else{
        return 'error'
      }
      }

    onNoClick(): void {
      this.dialogRef.close({ data: 'close' });
    }

  }
