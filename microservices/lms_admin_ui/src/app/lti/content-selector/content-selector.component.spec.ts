import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { ContentSelectorComponent } from './content-selector.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { LtiService } from '../service/lti.service';
import { of } from 'rxjs';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';

describe('ContentSelectorComponent', () => {
  let component: ContentSelectorComponent;
  let fixture: ComponentFixture<ContentSelectorComponent>;
  let ltiService : LtiService;
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, NgxSkeletonLoaderModule],
      declarations: [ ContentSelectorComponent ],
      providers : [MatSnackBar, 
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close', 'disableClose']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: '', extra_data:{} }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentSelectorComponent);
    component = fixture.componentInstance;
    ltiService = TestBed.inject(LtiService)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  // it('should observe getToolUrl method', ()=>{
  //   const mockResponse = {success:true, url: 'https://www.test.com/testing'}
  //   spyOn(ltiService, 'contentSelectionLaunch').and.returnValue(of({mockResponse}))
  //   component.getToolUrl()
  //   fixture.detectChanges()
  //   expect(component.loadingIframe).toBeTruthy()
  //   expect(ltiService.contentSelectionLaunch).toHaveBeenCalled()
  // })
});
