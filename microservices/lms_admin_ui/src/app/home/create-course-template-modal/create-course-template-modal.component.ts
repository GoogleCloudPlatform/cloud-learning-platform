import { Component, OnInit, Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HomeService } from '../service/home.service';
import { SuccessOverviewDialog } from '../home.component';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-create-course-template-modal',
  templateUrl: './create-course-template-modal.component.html',
  styleUrls: ['./create-course-template-modal.component.scss']
})
export class CreateCourseTemplateModalComponent implements OnInit {
  courseTemplateForm: UntypedFormGroup
  showProgressSpinner: boolean = false
  constructor(public dialog: MatDialog,public dialogRef: MatDialogRef<CreateCourseTemplateModalComponent>, private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService, @Inject(MAT_DIALOG_DATA) public courseTemplateModalData: any) { }

  ngOnInit(): void {
    console.log("data ", this.courseTemplateModalData)
    if (this.courseTemplateModalData.mode == 'Create') {
      this.courseTemplateForm = this.fb.group({
        name: this.fb.control({ value: this.courseTemplateModalData.init_data.name, disabled: false }, [Validators.required]),
        description: this.fb.control({ value: this.courseTemplateModalData.init_data.name, disabled: false }, [Validators.required]),
        // instructional_designer: this.fb.control('', [Validators.required, Validators.email]),
      });
    }
    else {
      this.courseTemplateForm = this.fb.group({
        name: this.fb.control({ value: this.courseTemplateModalData.init_data.name, disabled: false }, [Validators.required]),
        description: this.fb.control({ value: this.courseTemplateModalData.init_data.description, disabled: false }, [Validators.required]),
        // instructional_designer: this.fb.control({ value: this.courseTemplateModalData.init_data.instructional_designer, disabled: false }, [Validators.required, Validators.email]),
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
  onNoClick(): void {
    this.dialogRef.close({ data: 'close' });
  }

  createCourseTemplate() {
    this.showProgressSpinner = true


    if (this.courseTemplateModalData.mode == 'Edit') {
      this._HomeService.editCourseTemplate(this.courseTemplateForm.value, this.courseTemplateModalData.init_data.id).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Update course template', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });
        }
        else {
          this.openFailureSnackBar('Update course template', 'FAILED')
        }
        this.showProgressSpinner = false
      },
        (error: any) => {
          this.openFailureSnackBar('Update course template', 'FAILED')
          this.showProgressSpinner = false
        })
    }
    else {

      this._HomeService.createCourseTemplate(this.courseTemplateForm.value).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Create course template', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });

          const successOverviewDialogRef = this.dialog.open(SuccessOverviewDialog, {
            width: '500px',
            data: "Course template created"
          });


        }
        else {
          this.openFailureSnackBar('Create course template', 'FAILED')
        }
        this.showProgressSpinner = false
      }, (error: any) => {
        this.openFailureSnackBar('Create course template', 'FAILED')
        this.showProgressSpinner = false
        this.dialogRef.close({ data: 'success' });
      })
    }

  }


}
