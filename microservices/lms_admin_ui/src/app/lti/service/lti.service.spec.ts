import { TestBed } from '@angular/core/testing';

import { LtiService } from './lti.service';

describe('LtiService', () => {
  let service: LtiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LtiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
