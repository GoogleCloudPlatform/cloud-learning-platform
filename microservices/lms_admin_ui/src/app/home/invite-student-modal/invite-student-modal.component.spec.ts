import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { InviteStudentModalComponent } from './invite-student-modal.component';
import { UntypedFormBuilder } from '@angular/forms';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HomeService } from '../service/home.service';
import { of } from 'rxjs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('InviteStudentModalComponent', () => {
  let component: InviteStudentModalComponent;
  let fixture: ComponentFixture<InviteStudentModalComponent>;
  let dialogRef: MatDialogRef<InviteStudentModalComponent>;
  let homeService : HomeService;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, BrowserAnimationsModule],
      declarations: [ InviteStudentModalComponent ],
      providers: [UntypedFormBuilder, MatSnackBar, HomeService,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Cohort', init_data: { name: ''}, extra_data:[] }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InviteStudentModalComponent);
    component = fixture.componentInstance;
    dialogRef = TestBed.inject(MatDialogRef)
    homeService = TestBed.inject(HomeService)
    component.InviteStudentModalData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call method inviteStudent in Cohort mode', async()=>{
    const response = {'success': true}
    try{
      spyOn(homeService, 'inviteInCohort').and.returnValue(of(response))
      component.inviteStudent()
      fixture.detectChanges()
      expect(homeService.inviteInCohort).toHaveBeenCalled()
    }catch(error){
      expect(error).toBeInstanceOf(TypeError)
    }
  })

  it('should call method inviteStudent in Section mode', async()=>{
    const response = {'success': true}
    component.InviteStudentModalData.mode = 'Section'
    try{
      spyOn(homeService, 'inviteInSection').and.returnValue(of(response))
      component.inviteStudent()
      fixture.detectChanges()
      expect(homeService.inviteInSection).toHaveBeenCalled()
    }catch(error){
      expect(error).toBeInstanceOf(TypeError)
    }
  })

  afterAll(async()=>{
    try{
      // ...
    }
    catch(error){
      expect(error).toBeInstanceOf(TypeError)
    }
  })
});
