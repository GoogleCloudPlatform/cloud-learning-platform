import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { ContentSelectorComponent } from './content-selector.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('ContentSelectorComponent', () => {
  let component: ContentSelectorComponent;
  let fixture: ComponentFixture<ContentSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule],
      declarations: [ ContentSelectorComponent ],
      providers : [MatSnackBar, 
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close', 'disableClose']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: '', extra_data:{} }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
