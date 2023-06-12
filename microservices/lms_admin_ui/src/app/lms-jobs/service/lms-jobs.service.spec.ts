import { TestBed } from '@angular/core/testing';

import { JobsService } from './lms-jobs.service';

describe('JobsService', () => {
  let service: JobsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JobsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
