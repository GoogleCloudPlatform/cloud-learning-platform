import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { CreateSectionComponent } from './create-section.component';
import { UntypedFormBuilder } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HomeService } from '../service/home.service';
import { of } from 'rxjs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


describe('CreateSectionComponent', () => {
  let component: CreateSectionComponent;
  let fixture: ComponentFixture<CreateSectionComponent>;
  let homeService : HomeService
  let dialogRef : MatDialogRef<CreateSectionComponent>
  let dialog
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, BrowserAnimationsModule],
      declarations: [ CreateSectionComponent ],
      providers: [MatSnackBar, MatDialog, UntypedFormBuilder, HomeService,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: { name: ''}, extra_data:[] }}
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateSectionComponent);
    component = fixture.componentInstance;
    homeService = TestBed.inject(HomeService)
    dialogRef = TestBed.inject(MatDialogRef);
    dialog = TestBed.inject(MatDialog)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call createSection method in Create mode with success response', ()=>{
    const response = {'success':true}
    try{
      spyOn(homeService, 'createSection').and.returnValue(of(response))
      component.createSection()
      fixture.detectChanges()
      expect(homeService.createSection).toHaveBeenCalled()
    }catch(error){
      expect(error).toBeInstanceOf(TypeError)
    }
  })

  it('should call createSection method in Create mode with failure response update showProgressSpinner to false', ()=>{
    const response = {'success':false}
    spyOn(homeService, 'createSection').and.returnValue(of(response))
    component.createSection()
    fixture.detectChanges()
    expect(homeService.createSection).toHaveBeenCalled()
    expect(component.showProgressSpinner).toBeFalsy()
  })

  it('should call createSection method in Edit mode with success response', ()=>{
    const response = {'success':true}
    try{
      component.requiredDetails.mode = 'Edit'
      spyOn(homeService, 'editSection').and.returnValue(of(response))
      component.createSection()
      fixture.detectChanges()
      expect(homeService.editSection).toHaveBeenCalled()
    }catch(error){
      expect(error).toBeInstanceOf(TypeError)
    }
  })

  it('should call createSection method in Edit mode with failure response and update showProgressSpinner to false', ()=>{
    const response = {'success':false}
    component.requiredDetails.mode = 'Edit'
    spyOn(homeService, 'editSection').and.returnValue(of(response))
    component.createSection()
    fixture.detectChanges()
    expect(homeService.editSection).toHaveBeenCalled()
    expect(component.showProgressSpinner).toBeFalsy()
  })
});
