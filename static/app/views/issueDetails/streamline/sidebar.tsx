import styled from '@emotion/styled';

import ErrorBoundary from 'sentry/components/errorBoundary';
import {StreamlinedExternalIssueList} from 'sentry/components/group/externalIssuesList/streamlinedExternalIssueList';
import {space} from 'sentry/styles/space';
import type {Event} from 'sentry/types/event';
import type {Group} from 'sentry/types/group';
import type {Project} from 'sentry/types/project';
import StreamlinedActivitySection from 'sentry/views/issueDetails/streamline/activitySection';
import FirstLastSeenSection from 'sentry/views/issueDetails/streamline/firstLastSeenSection';

type Props = {
  group: Group;
  project: Project;
  event?: Event;
};

export default function StreamlinedSidebar({group, event, project}: Props) {
  return (
    <div>
      <FirstLastSeenSection group={group} />
      <StyledBreak />
      {event && (
        <ErrorBoundary mini>
          <StreamlinedExternalIssueList group={group} event={event} project={project} />
          <StyledBreak />
        </ErrorBoundary>
      )}
      <StreamlinedActivitySection group={group} />
    </div>
  );
}

const StyledBreak = styled('hr')`
  margin-top: ${space(1.5)};
  margin-bottom: ${space(1.5)};
  border-color: ${p => p.theme.border};
`;
