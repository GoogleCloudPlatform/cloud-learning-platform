import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { CourseTemplateComponent } from './course-template.component';
import { MatMenuModule } from '@angular/material/menu';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('CourseTemplateComponent', () => {
  let component: CourseTemplateComponent;
  let fixture: ComponentFixture<CourseTemplateComponent>;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, MatMenuModule, HttpClientTestingModule],
      declarations: [ CourseTemplateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CourseTemplateComponent);
    component = fixture.componentInstance;
    spyOn(component, 'getInstructionalDesigner')
    component.courseTemplateList = [{
      "id": "OPngzT66nOMgZbZ2wf",
      "name": "JW7",
      "description": "This is description",
      "admin": "lms_admin_teacher@dhodun.altostrat.com",
      "classroom_id": "6140574971",
      "classroom_code": "6zzuln",
      "classroom_url": "https://classroom.google.com/c/NjE0MANz0OTcx",
      "instructional_designer": 'null'
    }]
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
});
