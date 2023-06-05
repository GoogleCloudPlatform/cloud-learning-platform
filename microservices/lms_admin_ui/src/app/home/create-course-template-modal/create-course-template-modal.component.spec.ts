import { ComponentFixture, TestBed, inject } from '@angular/core/testing';
import { CreateCourseTemplateModalComponent } from './create-course-template-modal.component';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HomeService } from '../service/home.service';
import { UntypedFormBuilder } from '@angular/forms';
import { of } from 'rxjs';


describe('CreateCourseTemplateModalComponent', () => {
  let component: CreateCourseTemplateModalComponent;
  let fixture: ComponentFixture<CreateCourseTemplateModalComponent>;
  let dialog: MatDialog;
  let homeService: HomeService;
  let courseTemplateModalData
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, BrowserAnimationsModule],
      declarations: [ CreateCourseTemplateModalComponent ],
      providers: [MatDialog, MatSnackBar, HomeService, UntypedFormBuilder,
        { provide: MatDialogRef, useValue:  MatDialogRef<CreateCourseTemplateModalComponent>  },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: { name: ''}, extra_data:[]  } }
      ]
    })
    .compileComponents();
    fixture = TestBed.createComponent(CreateCourseTemplateModalComponent);
    component = fixture.componentInstance;
    homeService = TestBed.inject(HomeService);
    courseTemplateModalData = TestBed.inject(MAT_DIALOG_DATA)
    component.dialogRef = TestBed.inject(MatDialogRef)
    dialog = TestBed.inject(MatDialog)
    fixture.detectChanges();
  });



  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call createCourseTemplate', () => {
    const mockCreateResponse = {'success':true}
    spyOn(homeService, 'createCourseTemplate').and.returnValue(of(mockCreateResponse)); // Spy on the createCourseTemplate method
    component.createCourseTemplate();
    expect(homeService.createCourseTemplate).toHaveBeenCalled();
  });

  it('should call editCourseTemplate', () => {
    courseTemplateModalData.mode = 'Edit'
    const mockEditResponse = {'success':true}
    spyOn(homeService, 'editCourseTemplate').and.returnValue(of(mockEditResponse)); // Spy on the createCourseTemplate method
    component.createCourseTemplate();
    expect(homeService.editCourseTemplate).toHaveBeenCalled()
  });
});


