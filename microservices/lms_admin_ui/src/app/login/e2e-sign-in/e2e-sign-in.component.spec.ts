import { ComponentFixture, TestBed } from '@angular/core/testing';

import { E2eSignInComponent } from './e2e-sign-in.component';

describe('E2eSignInComponent', () => {
  let component: E2eSignInComponent;
  let fixture: ComponentFixture<E2eSignInComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ E2eSignInComponent ]
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
