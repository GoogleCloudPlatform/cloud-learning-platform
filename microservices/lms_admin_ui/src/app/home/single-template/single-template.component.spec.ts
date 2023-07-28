import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteLtiDialog, SingleTemplateComponent } from './single-template.component';
import { HomeService } from '../service/home.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { of } from 'rxjs'
import { By } from '@angular/platform-browser';
describe('SingleTemplateComponent', () => {
  let component: SingleTemplateComponent;
  let fixture: ComponentFixture<SingleTemplateComponent>;
  let homeService: HomeService
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule],
      declarations: [ SingleTemplateComponent, DeleteLtiDialog ],
      providers: [MatDialog,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: { name: ''}, extra_data:[] }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SingleTemplateComponent);
    component = fixture.componentInstance;
    homeService = TestBed.inject(HomeService)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call fetchDetails, test getCourseTemplate method and update courseTemplateDetails', ()=>{
    const contextId =  'id'
    const mockCourseTemplateDetails =  {
      "id": "JUgkiH5WHL0w9A08fe",
      "name": "JWT_test3",
      "description": "this is description",
      "admin": "lms_admin_teacher@dhdun.altostrat.com",
      "classroom_id": "6089170307",
      "classroom_code": "opbpmh",
      "classroom_url": "https://classroom.google.com/c/NjA5Ok3TcwMzA3"
    }
    spyOn(homeService, 'getCourseTemplate').and.returnValue(of(mockCourseTemplateDetails))
    component.fetchDetails(contextId)
    fixture.detectChanges()
    expect(homeService.getCourseTemplate).toHaveBeenCalled()
    expect(component.courseTemplateDetails).toEqual(mockCourseTemplateDetails)
    expect(component.loadCard).toBeTrue()
    const cohorElement = fixture.debugElement.query(By.css('mat-card-content .cohort-title .name'))
    expect(cohorElement.nativeElement.textContent).toBe('JWT_test3')
  })


  it('should call fetchLtiAssignments', ()=>{
    const contextId =  'id'
    const mockLtiAssignments = {
      "success": true,
      "message": "Data fetched successfully",
      "data": [
          {
              "id": "7Wme8sxPWth61bOYVR",
              "context_id": "JUgi3HWHoL0w9A08fe",
              "context_type": "course_template",
              "lti_assignment_title": "Test Assignment UI",
              "lti_content_item_id": "yFLMBn4gtkN9f9mxZo",
              "tool_id": "Jz9WXCW0pd5lDaa2q4",
              "course_work_id": "61136908897",
              "course_work_type": "course_work",
              "max_points": 60.0,
              "start_date": "2023-05-18T18:30:00+00:00",
              "end_date": "2023-06-14T18:30:00+00:00",
              "due_date": "2023-06-28T18:30:00+00:00"
          }
        ]
    }
    spyOn(homeService, 'getLtiAssignments').and.returnValue(of(mockLtiAssignments))
    component.fetchLtiAssignments(contextId)
    fixture.detectChanges()
    expect(homeService.getLtiAssignments).toHaveBeenCalled()
    expect(JSON.stringify(component.ltiAssignments)).toEqual(JSON.stringify(mockLtiAssignments.data))
    expect(component.loadTable).toBeTrue()
  })

  it('in child component DeleteLtiDialog should call deleteAssignment', ()=>{
    const fixture = TestBed.createComponent(DeleteLtiDialog);
    const component = fixture.componentInstance;
    component.deleteDialogData = TestBed.inject(MAT_DIALOG_DATA);
    const mockResponse = {'success':true}
    spyOn(homeService, 'deleteLtiAssignments').and.returnValue(of(mockResponse))
    component.deleteAssignment()
    expect(homeService.deleteLtiAssignments).toHaveBeenCalled()
  })
});
