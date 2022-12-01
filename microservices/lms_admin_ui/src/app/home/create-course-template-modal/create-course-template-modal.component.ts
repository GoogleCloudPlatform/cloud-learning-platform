import { Component, OnInit } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormControl, FormGroup, FormBuilder, Validators, Form } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HomeService } from '../service/home.service';

interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-create-course-template-modal',
  templateUrl: './create-course-template-modal.component.html',
  styleUrls: ['./create-course-template-modal.component.scss']
})
export class CreateCourseTemplateModalComponent implements OnInit {
  courseTemplateForm: FormGroup
  showProgressSpinner: boolean = false
  constructor(public dialogRef: MatDialogRef<CreateCourseTemplateModalComponent>, private fb: FormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService) { }

  ngOnInit(): void {
    this.courseTemplateForm = this.fb.group({
      name: this.fb.control('', [Validators.required]),
      description: this.fb.control('', [Validators.required]),
      instructional_designer: this.fb.control('', [Validators.required]),
      admin: this.fb.control('', [Validators.required]),
    });

  }
  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['green-snackbar'],
    });
  }
  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['red-snackbar'],
    });
  }
  onNoClick(): void {
    this.dialogRef.close({ data: 'close' });
  }

  createCourseTemplate() {
    this.showProgressSpinner = true
    this._HomeService.createCourseTemplate(this.courseTemplateForm.value).subscribe((res: any) => {
      if (res.success == true) {
        this.openSuccessSnackBar('Create course template', 'SUCCESS')
        this.dialogRef.close({ data: 'success' });
      }
      else {
        this.openFailureSnackBar('Create course template', 'FAILED')
      }
      this.showProgressSpinner = false
    }, (error: any) => {
      this.openFailureSnackBar('Create course template', 'FAILED')
      this.showProgressSpinner = false
    })

  }


}
