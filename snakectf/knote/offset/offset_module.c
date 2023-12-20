#include <linux/init.h>
#include <linux/module.h>
#include <linux/sched.h>

static int __init init_offsets(void) {
  printk(KERN_INFO "tasks offset wrt task_struct = 0x%lx\n",
         offsetof(struct task_struct, tasks));
  printk(KERN_INFO "cred offset wrt task_struct = 0x%lx\n",
         offsetof(struct task_struct, cred));
  printk(KERN_INFO "pid offset wrt task_struct = 0x%lx\n",
         offsetof(struct task_struct, pid));
  printk(KERN_INFO "uid offset wrt cred = 0x%lx\n", offsetof(struct cred, uid));
  printk(KERN_INFO "gid offset wrt cred = 0x%lx\n", offsetof(struct cred, gid));
  // Add information about other credentials inside the cred struct
  // ...

  return 0;
}

static void __exit cleanup_offsets(void) {
  // Cleanup code (if needed)
}

module_init(init_offsets);
