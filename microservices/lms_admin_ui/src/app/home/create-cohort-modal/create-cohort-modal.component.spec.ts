import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCohortModalComponent } from './create-cohort-modal.component';

describe('CreateCohortModalComponent', () => {
  let component: CreateCohortModalComponent;
  let fixture: ComponentFixture<CreateCohortModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateCohortModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCohortModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
