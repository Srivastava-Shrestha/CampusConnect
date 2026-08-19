<script setup>
defineProps({
  member: { type: Object, required: true }
})

const emit = defineEmits(['remove'])

function removeMember() {
  emit('remove')
}
</script>

<template>
  <div class="member-row">
    <div class="member-avatar">{{ member.initials }}</div>
    <div class="member-info">
      <p class="member-name">{{ member.name }}</p>
      <p class="member-sub">{{ member.sub }}</p>
    </div>
    <span class="member-role-badge" :class="member.role">{{ member.roleLabel }}</span>
    <button class="member-remove-btn" @click="removeMember">Remove</button>
  </div>
</template>
