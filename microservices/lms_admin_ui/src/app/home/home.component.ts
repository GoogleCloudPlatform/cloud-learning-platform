import { CreateCourseTemplateModalComponent } from './create-course-template-modal/create-course-template-modal.component';
import { Component, OnInit } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog'
import { CreateCohortModalComponent } from './create-cohort-modal/create-cohort-modal.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {
  searchText: string = '';
  constructor(public dialog: MatDialog) { }


  openDialog(): void {
    const dialogRef = this.dialog.open(CreateCohortModalComponent, {
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  openCourseTemplateDialog(): void {
    const dialogRef = this.dialog.open(CreateCourseTemplateModalComponent, {
      width: '500px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }


}
