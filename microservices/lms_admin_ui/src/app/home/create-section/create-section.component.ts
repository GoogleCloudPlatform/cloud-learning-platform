import { Component, OnInit, Inject } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HomeService } from '../service/home.service';

import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatLegacyChipInputEvent as MatChipInputEvent } from '@angular/material/legacy-chips';
import { SuccessOverviewDialog } from '../home.component';

interface LooseObject {
  [key: string]: any
}

@Component({
  selector: 'app-create-section',
  templateUrl: './create-section.component.html',
  styleUrls: ['./create-section.component.scss']
})
export class CreateSectionComponent implements OnInit {
  addSectionForm: UntypedFormGroup
  showProgressSpinner: boolean = false

  addOnBlur = true;
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  teachingStaff: any[] = [];
  constructor(public dialog: MatDialog,public dialogRef: MatDialogRef<CreateSectionComponent>, @Inject(MAT_DIALOG_DATA) public requiredDetails: any, private fb: UntypedFormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService) { }

  ngOnInit(): void {
    console.log('required det', this.requiredDetails)
    if (this.requiredDetails.mode == 'Create') {
      this.addSectionForm = this.fb.group({
        section_name: this.fb.control('', [Validators.required]),
        section_description: this.fb.control('', [Validators.required]),
        max_students:this.fb.control('', [Validators.required]),
        cohort: this.fb.control({ value: this.requiredDetails.extra_data.cohort_name, disabled: true }, [Validators.required]),
        course_template: this.fb.control({ value: this.requiredDetails.extra_data.course_template_name, disabled: true }, [Validators.required]),
        instructional_designer: this.fb.control({ value: this.requiredDetails.extra_data.instructional_desiner, disabled: true }, [Validators.required]),
        admin: this.fb.control({ value: this.requiredDetails.extra_data.admin, disabled: true }, [Validators.required]),
        // teachers: this.fb.control('')
      });
    }
    else {
      this.addSectionForm = this.fb.group({
        section_name: this.fb.control({ value: this.requiredDetails.init_data.section, disabled: false }, [Validators.required]),
        section_description: this.fb.control({ value: this.requiredDetails.init_data.description, disabled: false }, [Validators.required]),
        max_students: this.fb.control({value: this.requiredDetails.init_data.max_students, disabled: false}, [Validators.required]),
        cohort: this.fb.control({ value: this.requiredDetails.init_data.cohort_name, disabled: true }, [Validators.required]),
        course_template: this.fb.control({ value: this.requiredDetails.init_data.course_template_name, disabled: true }, [Validators.required]),
        instructional_designer: this.fb.control({ value: this.requiredDetails.init_data.instructional_desiner, disabled: true }, [Validators.required]),
        admin: this.fb.control({ value: this.requiredDetails.init_data.admin, disabled: true }, [Validators.required]),
        // teachers: this.fb.control('')
      });
      // this.teachingStaff = this.requiredDetails.init_data.teachers
    }
  }


  // add(event: MatChipInputEvent): void {
  //   const value = (event.value || '').trim();

  //   // Add our fruit
  //   if (value) {
  //     console.log(value)
  //     this.teachingStaff.push(value);
  //   }

  //   // Clear the input value
  //   event.chipInput!.clear();
  // }

  // remove(teachingStaff: any): void {
  //   const index = this.teachingStaff.indexOf(teachingStaff);

  //   if (index >= 0) {
  //     this.teachingStaff.splice(index, 1);
  //   }
  // }


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
  createSection() {
    this.showProgressSpinner = true
    // let tempTeacherList = []
    let sectionObj: LooseObject = {}
    sectionObj['description'] = this.addSectionForm.value.section_description.trim()
    sectionObj['cohort'] = this.requiredDetails.extra_data.cohort_id ? this.requiredDetails.extra_data.cohort_id : this.requiredDetails.init_data.cohort_id
    

    if (this.requiredDetails.mode == 'Edit') {
      console.log('sec obj', sectionObj)
      // this.requiredDetails.extra_data.instructional_desiner ? tempTeacherList.push(this.requiredDetails.extra_data.instructional_desiner) : tempTeacherList.push(this.requiredDetails.init_data.instructional_desiner)
      sectionObj['section_name'] = this.addSectionForm.value.section_name.trim()
      sectionObj['max_students'] = this.addSectionForm.value.max_students
      sectionObj['id'] = this.requiredDetails.init_data.section_id
      sectionObj['course_id'] = this.requiredDetails.init_data.classroom_id
      this._HomeService.editSection(sectionObj).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Update section', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });
        }
        else {
          this.openFailureSnackBar('Update section', 'FAILED')
          // this.dialogRef.close({ data: 'success' });
        }
        this.showProgressSpinner = false
      }, (error: any) => {
        this.openFailureSnackBar('Update section', 'FAILED')
        // this.dialogRef.close({ data: 'success' });
        this.showProgressSpinner = false
      })
    }
    else {
      sectionObj['name'] = this.addSectionForm.value.section_name.trim()
      sectionObj['max_students'] = this.addSectionForm.value.max_students
      sectionObj['course_template'] = this.requiredDetails.extra_data.course_template_id
      this._HomeService.createSection(sectionObj).subscribe((res: any) => {
        if (res.success == true) {
          this.openSuccessSnackBar('Create section', 'SUCCESS')
          this.dialogRef.close({ data: 'success' });
          const successOverviewDialogRef = this.dialog.open(SuccessOverviewDialog, {
            width: '500px',
            data: "Section creation in progress"
          });
        }
        else {
          this.openFailureSnackBar('Create section', 'FAILED')
          this.showProgressSpinner = false
          // this.dialogRef.close({ data: 'success' });
        }
        this.showProgressSpinner = false
      }, (error: any) => {
        this.openFailureSnackBar('Create section', 'FAILED')
        // this.dialogRef.close({ data: 'success' });
        this.showProgressSpinner = false
        
      })
      console.log('final obj', sectionObj)
    }
  }


}
