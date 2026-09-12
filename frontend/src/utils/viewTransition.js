import { flushSync } from 'react-dom'

// 화면(단계)이 바뀔 때 부드러운 크로스페이드로 전환되도록 도와주는 유틸.
// 브라우저가 View Transitions API(document.startViewTransition)를 지원하면
// 그걸 쓰고, 지원하지 않는 브라우저에서는 그냥 즉시 상태를 바꾼다(기존과 동일).
//
// React 18의 상태 업데이트는 기본적으로 비동기 배치 처리되기 때문에,
// startViewTransition의 콜백 안에서 그냥 setState를 호출하면 콜백이 끝난
// 시점에 아직 DOM이 안 바뀐 상태라 "Transition was aborted" 에러가 난다.
// flushSync로 감싸서 콜백 안에서 DOM 변경까지 동기적으로 끝나도록 만든다.
export function withViewTransition(updateState) {
  if (typeof document !== 'undefined' && document.startViewTransition) {
    const transition = document.startViewTransition(() => {
      flushSync(() => {
        updateState()
      })
    })
    // 트랜지션 "애니메이션" 자체가 (연속 클릭, 브라우저 환경 제약 등으로) 중간에
    // 스킵/중단되더라도 화면 전환(상태 변경)은 flushSync로 이미 끝난 뒤라
    // 기능상 문제는 없다. ready/finished가 reject돼도 콘솔에 안 보이는 에러로
    // 남지 않게 조용히 무시한다.
    transition.updateCallbackDone?.catch(() => {})
    transition.ready?.catch(() => {})
    transition.finished?.catch(() => {})
  } else {
    updateState()
  }
}
