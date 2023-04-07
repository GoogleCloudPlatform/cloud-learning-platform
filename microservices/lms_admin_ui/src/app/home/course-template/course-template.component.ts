import { CreateCourseTemplateModalComponent } from './../create-course-template-modal/create-course-template-modal.component';
import { Component, OnInit, Input } from '@angular/core';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CourseTemplateDetailsDialog } from '../home.component';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-course-template',
  templateUrl: './course-template.component.html',
  styleUrls: ['./course-template.component.scss']
})
export class CourseTemplateComponent implements OnInit {
  @Input() courseTemplateList: any[]
  constructor(public dialog: MatDialog,) { }
  selectedCourseTemplate: any
  ngOnInit(): void {
  }
  setSelected(courseTemplate: any) {
    this.selectedCourseTemplate = courseTemplate
  }
  openEditCourseTemplate() {
    let courseTemplateModalData: LooseObject = {}
    courseTemplateModalData['mode'] = 'Edit'
    courseTemplateModalData['init_data'] = this.selectedCourseTemplate
    courseTemplateModalData['extra_data'] = ''
    const dialogRef = this.dialog.open(CreateCourseTemplateModalComponent, {
      width: '500px',
      data: courseTemplateModalData
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(result)
      if (result.data == 'success') {
      }
    });
  }

  openClassroom(link: any) {
    window.open(link
      , '_blank');
  }

openDetailsDialogue(data:any){
  const CourseTemplateDetailsDialogRef = this.dialog.open(CourseTemplateDetailsDialog, {
    width: '600px',
    data: data
  });
}


}
