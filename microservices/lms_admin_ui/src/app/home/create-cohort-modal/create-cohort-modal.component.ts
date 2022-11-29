import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-create-cohort-modal',
  templateUrl: './create-cohort-modal.component.html',
  styleUrls: ['./create-cohort-modal.component.scss']
})
export class CreateCohortModalComponent implements OnInit {

  constructor(public dialogRef: MatDialogRef<CreateCohortModalComponent>) { }
  onNoClick(): void {
    this.dialogRef.close();
  }
  ngOnInit(): void {
  }

}
