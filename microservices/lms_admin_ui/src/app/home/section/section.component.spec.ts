import { ComponentFixture, TestBed, fakeAsync, tick  } from '@angular/core/testing';
import { DeleteOverviewDialog, DeleteSectionLtiDialog, SectionComponent, addTeacherDialog, staff } from './section.component';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HomeService } from '../service/home.service';
import { of } from 'rxjs';
import { By } from '@angular/platform-browser';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatTabsModule } from '@angular/material/tabs';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { UntypedFormBuilder, Validators } from '@angular/forms';


describe('SectionComponent', () => {
  let component: SectionComponent;
  let fixture: ComponentFixture<SectionComponent>;
  let homeService: HomeService;
  let addTeacherDialogData
  let mockCohort = {
    "id": "qhDMJeG3BNNme6l6TG6",
    "name": "Jwt test2",
    "description": "this is description",
    "start_date": "2023-05-14T00:00:00+00:00",
    "end_date": "2023-05-10T00:00:00+00:00",
    "registration_start_date": "2023-05-30T00:00:00+00:00",
    "registration_end_date": "2023-06-30T00:00:00+00:00",
    "max_students": 200,
    "enrolled_students_count": 5,
    "course_template": "course_templates/fHI8Hdb8WACPXsj5w2Y",
    "course_template_name": "JWT_test2"
  }
  let mockCourseTemplate = {
    "id": "fHI8Hdb8WAACPXsj5w2Y",
    "name": "JWT_test2",
    "description": "This is description",
    "admin": "lms_admin_teacher@dhodun.altostrat.com",
    "instructional_designer": "test_user_1@dhodun.altostrat.com",
    "classroom_id": "609587864272",
    "classroom_code": "q6quf6u",
    "classroom_url": "https://classroom.google.com/c/NjA5NTg3ODY0Mjcy"
  }
  let mockSections = {
    "success": true,
    "message": "Success list",
    "data": [
        {
            "id": "YgrAS5xryPuEHjtJzTl",
            "name": "JWT_test2",
            "section": "section 2",
            "description": "This is updated create section test",
            "classroom_id": "61225119376",
            "classroom_code": "ngz2pxh",
            "classroom_url": "https://classroom.google.com/c/NjEyMjUMTE5Mzc2",
            "course_template": "course_templates/fHI8Hdb8WACPXsj5w2Y",
            "cohort": "cohorts/qhDMJeG3BNYme6l6TG6",
            "status": "ACTIVE",
            "enrollment_status": "OPEN",
            "enrolled_students_count": 51,
            "max_students": 1000
        },
        {
            "id": "eTj7TO5YKYTRRaKZLu7",
            "name": "JWT_test2",
            "section": "section 2",
            "description": "This is updated create section test",
            "classroom_id": "61223527725",
            "classroom_code": "nj3vb3b",
            "classroom_url": "https://classroom.google.com/c/NjEyMM1Mjc0NzI1",
            "course_template": "course_templates/fHI8Hdb8WACPXsj5w2Y",
            "cohort": "cohorts/qhDMJeG3BNYNe6l6TG6",
            "status": "PROVISIONING",
            "enrollment_status": "CLOSED",
            "enrolled_students_count": 49,
            "max_students": 1000
        }
      ]
    }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ MatLegacyDialogModule, HttpClientTestingModule,MatSelectModule,MatInputModule, MatTabsModule, BrowserAnimationsModule,NgxSkeletonLoaderModule],
      declarations: [ SectionComponent, addTeacherDialog , DeleteOverviewDialog],
      providers: [ MatSnackBar, MatDialog,UntypedFormBuilder,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: { name: ''}, extra_data:[] }}
      ],
      schemas:[CUSTOM_ELEMENTS_SCHEMA]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SectionComponent);
    component = fixture.componentInstance;
    homeService = TestBed.inject(HomeService);
    addTeacherDialogData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize component with default values', () => {
    let expectedColumns = ['name','email','role','status','action']
    expect(component.displayedColumns).toEqual(expectedColumns);
  });

  it('should call getCohortDetails method', async() => {
    let id = 'fHI8H'
    spyOn(homeService, 'getCohort').and.returnValue(of())
    component.getCohortDetails(id)
    fixture.detectChanges()
    expect(homeService.getCohort).toHaveBeenCalled()
  });

  it('should call getCohortDetails method and update cohortDetails', async() => {
    let id = 'fHI8H'
    spyOn(homeService, 'getCohort').and.returnValue(of(mockCohort))
    component.getCohortDetails(id)
    fixture.detectChanges()
    expect(homeService.getCohort).toHaveBeenCalled()
    expect(component.cohortDetails).toEqual(mockCohort)
  });

  it('should call getCourseTemplateDetails method and update courseTemplateDetails', async() => {
    component.cohortDetails = mockCohort
    fixture.detectChanges()
    spyOn(homeService, 'getCourseTemplate').and.returnValue(of(mockCourseTemplate))
    component.getCourseTemplateDetails(mockCohort.id)
    fixture.detectChanges()
    expect(homeService.getCourseTemplate).toHaveBeenCalled()
    expect(component.courseTemplateDetails).toEqual(mockCourseTemplate)
  });

  it('should call getSectionList method and update sectionDetails', async() => {
    component.cohortDetails = mockCohort
    spyOn(homeService, 'getSectionList').and.returnValue(of(mockSections))
    component.getSectionList(mockCohort.id)
    fixture.detectChanges()
    expect(homeService.getSectionList).toHaveBeenCalled()
    expect(JSON.stringify(component.sectionDetails)).toEqual(JSON.stringify(mockSections.data))
  });

  it('should call getSectionList method and update loadSection to false', async() => {
    component.cohortDetails = mockCohort
    spyOn(homeService, 'getSectionList').and.returnValue(of(mockSections))
    component.getSectionList(mockCohort.id)
    fixture.detectChanges()
    expect(component.loadSection).toBeFalse()
  });

  it('should call createTableData and update selectedSection on section select', async() => {
    component.loadSection = false
    component.sectionDetails = mockSections.data
    component.selectedSection = component.sectionDetails[0]

    spyOn(component, 'createTableData')
    fixture.detectChanges()

    const matSelect = fixture.debugElement.query(By.css('mat-select'))
    matSelect.nativeElement.click()
    fixture.detectChanges();

    const matOptions = fixture.debugElement.queryAll(By.css('mat-option'))
    const lastOptionIndex = matOptions.length-1
    matOptions[lastOptionIndex].nativeElement.click()
    fixture.detectChanges();

    expect(component.createTableData).toHaveBeenCalled()

    expect(component.selectedSection).toEqual(component.sectionDetails[lastOptionIndex])

    const managementTitleElement  = fixture.debugElement.query(By.css('.section-management span'))
    expect(managementTitleElement.nativeElement.textContent).toBe(component.selectedSection.section+ ' management')
  })
  
  it('should call getSectionStudents and update studentTableData', ()=>{
    const mockSectionStudents = {
      "success": true,
      "message": "Success",
      "data": [
          {
              "user_id": "En4SSjm3tfT8Cq4nog",
              "first_name": "clp1",
              "last_name": "clplast",
              "email": "clplstestuer1@gmail.com",
              "user_type": "learner",
              "status": "active",
              "gaia_id": "1106175590637510026",
              "photo_url": "https://lh3.googleusercontent.com/a/AGNmyxbZ2aojvvF8y3_9qUS0i5DOB1x17YBNtaXbj=s100",
              "course_enrollment_id": "eJxado5E4hDWwbyyMQY",
              "invitation_id": null,
              "section_id": "YgrASxryPuEHHjtJzTl",
              "cohort_id": "qhDJG3BNYNme6l6TG6",
              "classroom_id": "62252119376",
              "enrollment_status": "active",
              "classroom_url": "https://classroom.google.com/c/NjEyMjUyE5Mzc2"
          }
      ]
    }
    component.selectedSection = mockSections.data[0]
    spyOn(homeService,'getStudentsInSection').and.returnValue(of(mockSectionStudents))
    component.getSectionStudents()
    fixture.detectChanges()
    expect(homeService.getStudentsInSection).toHaveBeenCalled()
    expect(JSON.stringify(component.studentTableData)).toEqual(JSON.stringify(mockSectionStudents.data))
    expect(component.studentTableLoader).toBeFalsy()
  })

  it('should call getSectionTeachers and update teacherTableData', ()=>{
    const mockSectionTeacher = {
      "success": true,
      "message": "Success",
      "data": [
          {
              "user_id": "5T6djbCfdPMbznOKI5",
              "first_name": "test_user_2",
              "last_name": "test_user_2",
              "email": "test_ser_2@dhdun.altostrat.com",
              "user_type": "faculty",
              "status": "active",
              "gaia_id": "104292872696788454",
              "photo_url": "https://lh3.googleusrcontent.com/a/default-user",
              "course_enrollment_id": "Abt5MhvoW9ZKWZFyO",
              "invitation_id": "",
              "section_id": "YgrAS5xryuEHHJzTl",
              "cohort_id": "qhDMeG3NYNme6l6TG6",
              "classroom_id": "6125119376",
              "enrollment_status": "active",
              "classroom_url": "https://classroom.google.com/c/NjEyMjUyME5Mzc2"
          }
        ]
      }
    let mockTeacherTableData = []
    for (let x of mockSectionTeacher.data) {
      let staffObj: staff = { name: '', email: '', role: '', status:'' }
      staffObj.name = x.first_name+' '+x.last_name
      staffObj.email = x.email
      staffObj.role = 'Teaching Staff'
      staffObj.status = x.status
      mockTeacherTableData.push(staffObj)
    }
    component.selectedSection = mockSections.data[0]
    spyOn(homeService,'getTeachersInSection').and.returnValue(of(mockSectionTeacher))
    component.getSectionTeachers()
    fixture.detectChanges()
    expect(homeService.getTeachersInSection).toHaveBeenCalled()
    expect(JSON.stringify(component.teacherTableData)).toEqual(JSON.stringify(mockTeacherTableData))
    expect(component.teacherTableLoader).toBeFalsy()

    
  })

  it('should call getCourseworkDetails and update courseworkTable', ()=>{
    const mockTestWorkData = {
      "success": true,
      "message": "Success",
      "data": [
          {
              "courseId": "61225211976",
              "courseWorkId": "61240764097",
              "title": "New assignment",
              "state": "PUBLISHED",
              "creationTime": "2023-05-31T09:34:36.003Z",
              "materials": [
                  {
                      "link": {
                          "url": "https://core-learning-services-dev.cloudpssolutions.com/classroom-shim/api/v1/launch?lti_assignment_id=NluSaWeHbd87r5SjFg",
                          "title": "new assignment",
                          "thumbnailUrl": "https://classroom.google.com/webthumbnail?url=https://core-learning-services-dev.cloudpssolutions.com/classroom-shim/api/v1/launch?lti_assignment_id%3DNWluSaWHbdH7r5SjFg"
                      }
                  }
              ]
          },
          {
              "courseId": "61225119376",
              "courseWorkId": "62252101482",
              "title": "This is quizeee",
              "state": "PUBLISHED",
              "creationTime": "2023-05-30T14:42:27.279Z",
              "materials": [
                  {
                      "form": {
                          "formUrl": "https://docs.google.com/forms/d/e/1FAIpQLSc32GJlT_w2qLKlPpM0YAGBxOlMY36KR9bKre6YpGIg5Mg/viewform",
                          "title": "e2e_form1",
                          "thumbnailUrl": "https://lh5.googleusercontent.com/Fr67ll-cV3hAaD7DtCpkTyYBIPoZcu_1OET8ckfuEY3NNFCwJTGnV3RaHQ2M5csJ8AAY4Vz0=w90-h90-p"
                      }
                  }
              ]
          },
          {
              "courseId": "61225211976",
              "courseWorkId": "61225101463",
              "title": "DOCUMENT ",
              "state": "PUBLISHED",
              "creationTime": "2023-05-30T14:42:21.209Z",
              "materials": [
                  {
                      "driveFile": {
                          "driveFile": {
                              "id": "1_sYRog0oDg-Ed0v66_c3w-U6feOvBWI-0ydQ8iwE",
                              "title": "test1",
                              "alternateLink": "https://docs.google.com/document/d/1_sYRogP0oDg-Ed0v6K_c3w-U6f5eOvBI-0ydQ8iwE/edit?usp=drive_web",
                              "thumbnailUrl": "https://lh3.google.com/zjWOCqaeLMbyp8ucqOIfwCtz2Md9xic3RnKVOsDk7nU7OuIGLV8aplP9yiUuhrD10_2-qXu1SPQ15YlINrsfXTKdNWuiCp2Ad=s200"
                          },
                          "shareMode": "VIEW"
                      }
                  },
                  {
                      "youtubeVideo": {
                          "id": "KGMf31LUc0",
                          "title": "Math Antics - Basic Division",
                          "alternateLink": "https://www.youtube.com/watch?v=KGMf31LUc0",
                          "thumbnailUrl": "https://i.ytimg.com/vi/KGMf31LUc0/default.jpg"
                      }
                  }
              ]
          }
      ]
    }
    component.selectedSection = mockSections.data[0]
    spyOn(homeService, 'getCourseworkDetails').and.returnValue(of(mockTestWorkData))
    component.getCourseworkDetails()
    fixture.detectChanges()
    expect(homeService.getCourseworkDetails).toHaveBeenCalled()
    let mockCourseworkTable = []
    for (let x of mockTestWorkData.data){
      x['status'] = 'import'
      mockCourseworkTable.push(x)
    }
    expect(JSON.stringify(component.courseworkTable)).toBe(JSON.stringify(mockCourseworkTable))
  })

  it('should call getLtiAssignmentsDetails and update ltiAssignmentsTableData', ()=>{
    const mockLtiAssignData = {
      "success": true,
      "message": "Data fetched successfully",
      "data": [
          {
              "id": "NWluSaWHb8H7r5SjFg",
              "context_id": "YgrA5xyPuEHHjtJzTl",
              "context_type": "section",
              "lti_assignment_title": "New assignment",
              "lti_content_item_id": "BQzZ4WtgxRlQ9dhHxO",
              "tool_id": "Jz9WCWupod5lDaa2q4",
              "course_work_id": "6123064097",
              "max_points": 100.0,
              "start_date": "2023-05-30T18:30:00+00:00",
              "end_date": "2023-07-30T18:30:00+00:00",
              "due_date": "2023-07-30T18:30:00+00:00"
          }
      ]
    }
    component.selectedSection = mockSections.data[0]
    spyOn(homeService, 'getLtiAssignments').and.returnValue(of(mockLtiAssignData))
    component.getLtiAssignmentsDetails()
    fixture.detectChanges()
    expect(homeService.getLtiAssignments).toHaveBeenCalled()
    expect(JSON.stringify(component.ltiAssignmentsTableData)).toBe(JSON.stringify(mockLtiAssignData.data))
    expect(component.ltiAssignmentTableLoader).toBeFalsy()
  })

  it('should call callGradeImport and update', ()=>{
    component.selectedSection = mockSections.data[0]
    component.courseworkTable = [{
      'status': 'import',
      "courseId": "61225211976",
      "courseWorkId": "61240764097",
      "title": "New assignment",
      "state": "PUBLISHED",
      "creationTime": "2023-05-31T09:34:36.003Z",
      "materials": []
    }]
    spyOn(homeService, 'gradeImport').and.returnValue(of(''))
    const rowNumber = 0
    const courseworkId = 'ABC'
    component.callGradeImport(rowNumber, courseworkId) // passing dummy rowNumber and courseworkId
    fixture.detectChanges()
    expect(homeService.gradeImport).toHaveBeenCalled();
    expect(component.courseworkTable[rowNumber].status).toBe('import_done')
    expect(component.disableCourseworkAction).toBeFalsy()
  })

  it('In addTeacherDialog component should call addTeacher and update showProgressSpinner to false',()=>{
    let fixture = TestBed.createComponent(addTeacherDialog);
    let component = fixture.componentInstance;
    let fb = TestBed.inject(UntypedFormBuilder)
    component.dialogRef = TestBed.inject(MatDialogRef)
    component.addTeacherDialogData.id = '12345'
    component.addTeacherForm = fb.group({
      email: fb.control('', [Validators.required, Validators.email])
    })
    spyOn(homeService, 'addTeacher').and.returnValue(of({'success':true}))
    component.addTeacher()
    fixture.detectChanges()
    expect(homeService.addTeacher).toHaveBeenCalled()
    expect(component.showProgressSpinner).toBeFalsy()
  })

  it('In DeleteOverviewDialog component should call delete and deleteStudent/deleteTeacher',()=>{
    let fixture = TestBed.createComponent(DeleteOverviewDialog);
    let component = fixture.componentInstance;
    component.deleteDialogData = TestBed.inject(MAT_DIALOG_DATA)
    component.deleteDialogData.type = 'student'
    component.dialogRef = TestBed.inject(MatDialogRef)

    spyOn(homeService, 'deleteStudent').and.returnValue(of({success:true}))
    component.delete()
    fixture.detectChanges()
    expect(homeService.deleteStudent).toHaveBeenCalled()

    spyOn(homeService, 'deleteTeacher').and.returnValue(of({success:true}))
    component.deleteDialogData.type = ''
    fixture.detectChanges()
    component.delete()
    expect(homeService.deleteTeacher).toHaveBeenCalled()
  })

  it('In DeleteSectionLtiDialog component should call deleteAssignment',()=>{
    let fixture = TestBed.createComponent(DeleteSectionLtiDialog);
    let component = fixture.componentInstance;
    spyOn(homeService, 'deleteLtiAssignments').and.returnValue(of({success:true}))
    component.deleteAssignment()
    fixture.detectChanges()
    expect(homeService.deleteLtiAssignments).toHaveBeenCalled()
  })
  
});
