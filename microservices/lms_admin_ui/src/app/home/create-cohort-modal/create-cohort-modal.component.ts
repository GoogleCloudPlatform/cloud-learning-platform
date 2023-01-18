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
  constructor(public dialogRef: MatDialogRef<CreateCohortModalComponent>, @Inject(MAT_DIALOG_DATA) public cohortModalData: any, private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService) { }
  ngOnInit(): void {
    console.log("data ", this.cohortModalData)
    if (this.cohortModalData.mode == 'Create') {
      console.log('data', this.cohortModalData)
      this.createCohortForm = this.fb.group({
        name: this.fb.control('', [Validators.required]),
        description: this.fb.control('', [Validators.required]),
        start_date: this.fb.control('', [Validators.required]),
        end_date: this.fb.control('', [Validators.required]),
        registration_start_date: this.fb.control('', [Validators.required]),
        registration_end_date: this.fb.control('', [Validators.required]),
        max_students: this.fb.control('', [Validators.required]),
        course_template_id: this.fb.control('', [Validators.required]),
      });
    }
    else {
      console.log('edit data', this.cohortModalData, this.cohortModalData.init_data.name)
      this.createCohortForm = this.fb.group({
        name: this.fb.control({ value: this.cohortModalData.init_data.name, disabled: false }, [Validators.required]),
        description: this.fb.control({ value: this.cohortModalData.init_data.description, disabled: false }, [Validators.required]),
        start_date: this.fb.control({ value: this.cohortModalData.init_data.start_date, disabled: false }, [Validators.required]),
        end_date: this.fb.control({ value: this.cohortModalData.init_data.end_date, disabled: false }, [Validators.required]),
        registration_start_date: this.fb.control({ value: this.cohortModalData.init_data.registration_start_date, disabled: false }, [Validators.required]),
        registration_end_date: this.fb.control({ value: this.cohortModalData.init_data.registration_end_date, disabled: false }, [Validators.required]),
        max_students: this.fb.control({ value: this.cohortModalData.init_data.max_students, disabled: false }, [Validators.required]),
        course_template_id: this.fb.control({ value: this.cohortModalData.init_data.course_template_name, disabled: true }, [Validators.required]),
      });
    }
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
    if (this.cohortModalData.mode == 'Edit') {
      this._HomeService.editCohort(this.createCohortForm.value, this.cohortModalData.init_data.id).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Update cohort', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });
        }
        else {
          this.openFailureSnackBar('Update cohort', 'FAILED')
        }
        this.showProgressSpinner = false
      }, (error: any) => {
        this.openFailureSnackBar('Update cohort', 'FAILED')
        this.showProgressSpinner = false
      })
    }
    else {
      this._HomeService.createCohort(this.createCohortForm.value).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Create cohort', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });
        }
        else {
          this.openFailureSnackBar('Create cohort', 'FAILED')
        }
        this.showProgressSpinner = false
      }, (error: any) => {
        this.openFailureSnackBar('Create cohort', 'FAILED')
        this.showProgressSpinner = false
      })
    }
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'close' });
  }


}
