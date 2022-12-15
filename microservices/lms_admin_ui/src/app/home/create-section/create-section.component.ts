import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FormControl, FormGroup, FormBuilder, Validators, Form } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HomeService } from '../service/home.service';

import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';

interface LooseObject {
  [key: string]: any
}

@Component({
  selector: 'app-create-section',
  templateUrl: './create-section.component.html',
  styleUrls: ['./create-section.component.scss']
})
export class CreateSectionComponent implements OnInit {
  addSectionForm: FormGroup
  showProgressSpinner: boolean = false

  addOnBlur = true;
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  teachingStaff: any[] = [];
  constructor(public dialogRef: MatDialogRef<CreateSectionComponent>, @Inject(MAT_DIALOG_DATA) public requiredDetails: any, private fb: FormBuilder,
    private _snackBar: MatSnackBar, private _HomeService: HomeService) { }

  ngOnInit(): void {
    console.log('required', this.requiredDetails)
    this.addSectionForm = this.fb.group({
      section_name: this.fb.control('', [Validators.required]),
      section_description: this.fb.control('', [Validators.required]),
      cohort: this.fb.control({ value: this.requiredDetails.cohort_name, disabled: true }, [Validators.required]),
      course_template: this.fb.control({ value: this.requiredDetails.course_template_name, disabled: true }, [Validators.required]),
      instructional_designer: this.fb.control({ value: this.requiredDetails.instructional_desiner, disabled: true }, [Validators.required]),
      admin: this.fb.control({ value: this.requiredDetails.admin, disabled: true }, [Validators.required]),
      teaching_staff: this.fb.control('')
    });
  }


  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our fruit
    if (value) {
      console.log(value)
      this.teachingStaff.push(value);
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  remove(teachingStaff: any): void {
    const index = this.teachingStaff.indexOf(teachingStaff);

    if (index >= 0) {
      this.teachingStaff.splice(index, 1);
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
  createSection() {
    // console.log(this.teachingStaff)
    // console.log(this.addSectionForm.value)
    this.showProgressSpinner = true
    let tempTeacherList = []
    let sectionObj: LooseObject = {}
    sectionObj['name'] = this.addSectionForm.value.section_name.trim()
    sectionObj['description'] = this.addSectionForm.value.section_description.trim()
    sectionObj['course_template'] = this.requiredDetails.course_template_uuid
    sectionObj['cohort'] = this.requiredDetails.cohort_uuid
    tempTeacherList.push(this.requiredDetails.instructional_desiner)
    for (let x of this.teachingStaff) {
      tempTeacherList.push(x)
    }
    sectionObj['teachers_list'] = tempTeacherList

    this._HomeService.createSection(sectionObj).subscribe((res: any) => {
      if (res.status == 'Success') {
        this.openSuccessSnackBar('Create section', 'SUCCESS')
        this.dialogRef.close({ data: 'success' });
      }
      else {
        this.openFailureSnackBar('Create section', 'FAILED')
      }
      this.showProgressSpinner = false
    }, (error: any) => {
      this.openFailureSnackBar('Create section', 'FAILED')
      this.showProgressSpinner = false
    })
    console.log('final obj', sectionObj)
  }


}
