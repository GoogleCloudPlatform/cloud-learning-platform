import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BatchJobsListComponent } from './batch-jobs-list.component';

describe('BatchJobsListComponent', () => {
  let component: BatchJobsListComponent;
  let fixture: ComponentFixture<BatchJobsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BatchJobsListComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BatchJobsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
