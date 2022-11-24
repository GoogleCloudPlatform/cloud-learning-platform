import { Component, OnInit } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-create-course-template-modal',
  templateUrl: './create-course-template-modal.component.html',
  styleUrls: ['./create-course-template-modal.component.scss']
})
export class CreateCourseTemplateModalComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<CreateCourseTemplateModalComponent>) { }
  onNoClick(): void {
    this.dialogRef.close();
  }
  ngOnInit(): void {
  }

}
