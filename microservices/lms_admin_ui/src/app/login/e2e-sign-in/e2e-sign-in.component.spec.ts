import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { E2eSignInComponent } from './e2e-sign-in.component';
import { AngularFireModule } from '@angular/fire/compat';
import { environment } from 'src/environments/environment';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { UntypedFormBuilder } from '@angular/forms';

describe('E2eSignInComponent', () => {
  let component: E2eSignInComponent;
  let fixture: ComponentFixture<E2eSignInComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule ,AngularFireModule.initializeApp(environment.firebase)],
      declarations: [ E2eSignInComponent ],
      providers: [MatSnackBar, UntypedFormBuilder]
    })
    .compileComponents();

    fixture = TestBed.createComponent(E2eSignInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
