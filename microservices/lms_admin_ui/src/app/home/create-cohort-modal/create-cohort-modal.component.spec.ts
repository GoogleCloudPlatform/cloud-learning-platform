import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CreateCohortModalComponent } from './create-cohort-modal.component';
import { HomeService } from '../service/home.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { UntypedFormBuilder } from '@angular/forms';
import { of } from 'rxjs';

describe('CreateCohortModalComponent', () => {
  let component: CreateCohortModalComponent;
  let fixture: ComponentFixture<CreateCohortModalComponent>;
  let homeService: HomeService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, BrowserAnimationsModule, HttpClientTestingModule],
      declarations: [ CreateCohortModalComponent ],
      providers: [UntypedFormBuilder,MatSnackBar,
        { provide: MatDialogRef, useValue:  MatDialogRef<CreateCohortModalComponent>  },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: { name: ''}, extra_data:[]  } }
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCohortModalComponent);
    component = fixture.componentInstance;
    component.cohortModalData = TestBed.inject(MAT_DIALOG_DATA)
    homeService = TestBed.inject(HomeService);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('it should call createCohort method',async()=>{
    const mockCreateCohortResponse = {'success':false}
    spyOn(homeService, 'createCohort').and.returnValue(of(mockCreateCohortResponse))
    component.createCohort()
    fixture.detectChanges()
    expect(homeService.createCohort).toHaveBeenCalled();
    expect(component.showProgressSpinner).toBeFalsy()
  })

  it('it should call editCohort method',async()=>{
    const mockCreateCohortResponse = {'success':false}
    component.cohortModalData.mode = 'Edit'
    spyOn(homeService, 'editCohort').and.returnValue(of(mockCreateCohortResponse))
    component.createCohort()
    fixture.detectChanges()
    expect(homeService.editCohort).toHaveBeenCalled();
    expect(component.showProgressSpinner).toBeFalsy()
  })

});
