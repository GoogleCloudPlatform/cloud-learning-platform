import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HomeComponent } from './home.component';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HomeService } from './service/home.service';
import { of } from 'rxjs/internal/observable/of';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;
  let homeService: HomeService;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule],
      declarations: [ HomeComponent ],
      providers: [MatDialog, MatDialogRef, HomeService]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    homeService = TestBed.inject(HomeService);
    fixture.detectChanges();
  });


  it('should create', () => {
    expect(component).toBeTruthy();
  });


  it('should call getCohortList', () => {
    const mockCohortValue = 'Mocked Value'
    spyOn(homeService, 'getCohortList').and.returnValue(of(mockCohortValue)); // Create a spy on getCohortList method
    component.getCohortList();
    expect(homeService.getCohortList).toHaveBeenCalled();
  });


  it('should call getCohortList and update cohortList', () => {
    const mockCohortResponse = {
      "success": true,
      "message": "Successfully get the Cohort list",
      "cohort_list": [
          {
              "id": "qhDMJeG3YNmel6TG6",
              "name": "Jwt test2",
              "description": "this is description",
              "start_date": "2023-05-14T00:00:00+00:00",
              "end_date": "2023-05-10T00:00:00+00:00",
              "registration_start_date": "2023-05-30T00:00:00+00:00",
              "registration_end_date": "2023-06-30T00:00:00+00:00",
              "max_students": 200,
              "enrolled_students_count": 2,
              "course_template": "course_templates/fHI8HdbACPXsj5w2Y",
              "course_template_name": "JWT_test2"
        }
      ]
    }
    spyOn(homeService, 'getCohortList').and.returnValue(of(mockCohortResponse)); // Create a spy on getCohortList method
    component.getCohortList();
    expect(component.cohortList).toBe(mockCohortResponse.cohort_list)
  });


  it('should call method getCourseTemplateList', () => {
    spyOn(homeService, 'getCourseTemplateList').and.returnValue(of('Mocked Value')); // Create a spy on getCourseTemplateList method
    component.getCourseTemplateList();
    expect(homeService.getCourseTemplateList).toHaveBeenCalled();
  });


  it('should call method getCourseTemplateList and update courseTemplateList', () => {
    const mockCourseResponse = {
      "success": true,
      "message": "Success list",
      "course_template_list": []
    }
    spyOn(homeService, 'getCourseTemplateList').and.returnValue(of('Mocked Value')); // Create a spy on getAllSectionsList method
    component.getCourseTemplateList();
    expect(component.courseTemplateList).toEqual(mockCourseResponse.course_template_list);
  });


  it('should call method getAllSectionsList', () => {
    spyOn(homeService, 'getAllSectionList').and.returnValue(of('Mocked Value')); // Create a spy on getAllSectionsList method
    component.getAllSectionsList();
    expect(homeService.getAllSectionList).toHaveBeenCalled();
  });


  it('should call method getAllSectionsList and update sectionList', () => {
    const mockSectionResponse = {
      "success": true,
      "message": "Success list",
      "data": [
          {
              "id": "PEnNVKSmPp4zn9bbd",
              "name": "Test LTI",
              "section": "Test section 1",
              "description": "test section 1 desc",
              "classroom_id": "612166192",
              "classroom_code": "426ocr",
              "classroom_url": "https://classroom.google.com/c/NjEMAOTc2MTky",
              "course_template": "course_templates/cNcuWUQ0ddE7s9zcA",
              "cohort": "cohorts/9Oe5ncilP56pqWHm",
              "status": "ACTIVE",
              "enrolled_students_count": 0
          }
        ]
    }
    spyOn(homeService, 'getAllSectionList').and.returnValue(of(mockSectionResponse)); // Create a spy on getAllSectionsList method
    component.getAllSectionsList();
    expect(component.sectionList).toBe(mockSectionResponse.data);
  });
});
