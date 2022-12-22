import { Component, OnInit, Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HomeService } from '../service/home.service';

@Component({
  selector: 'app-create-cohort-modal',
  templateUrl: './create-cohort-modal.component.html',
  styleUrls: ['./create-cohort-modal.component.scss']
})
export class CreateCohortModalComponent implements OnInit {
  createCohortForm: UntypedFormGroup
  showProgressSpinner: boolean = false
  constructor(public dialogRef: MatDialogRef<CreateCohortModalComponent>, @Inject(MAT_DIALOG_DATA) public courseTemplateData: any, private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService) { }
  ngOnInit(): void {
    console.log('data', this.courseTemplateData)
    this.createCohortForm = this.fb.group({
      name: this.fb.control('', [Validators.required]),
      description: this.fb.control('', [Validators.required]),
      start_date: this.fb.control('', [Validators.required]),
      end_date: this.fb.control('', [Validators.required]),
      registration_start_date: this.fb.control('', [Validators.required]),
      registration_end_date: this.fb.control('', [Validators.required]),
      max_students: this.fb.control('', [Validators.required]),
      course_template_uuid: this.fb.control('', [Validators.required]),
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

  createCohort() {
    this.showProgressSpinner = true
    this._HomeService.createCohort(this.createCohortForm.value).subscribe((res: any) => {
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

  onNoClick(): void {
    this.dialogRef.close({ data: 'close' });
  }


}
